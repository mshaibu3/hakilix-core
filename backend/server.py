from __future__ import annotations
import time
import json
import random
import logging
import uuid
import os
from collections import deque
from datetime import datetime
from typing import List, Optional
from enum import Enum
from statistics import mean

import uvicorn
from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Backend")

app = FastAPI(title="Hakilix Core Enterprise", version="22.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- DATA MODELS (Adapted from hakilix_single.py) ---
class SensorFrame(BaseModel):
    timestamp: str
    vertical_accel_g: float
    posture_angle_deg: float
    movement_energy: float
    zone: Optional[str] = None
    is_in_bed: bool = False
    step_rate_hz: Optional[float] = 0.0

class SensorWindow(BaseModel):
    patient_id: str
    frames: List[SensorFrame]

class FallDetectionResult(BaseModel):
    is_fall: bool
    confidence: float
    severity: str
    reason: List[str]
    flag_virtual_ward_review: bool
    time_to_recover_seconds: Optional[float] = None

class ActivityState(BaseModel):
    timestamp: datetime
    label: str
    confidence: float
    is_potential_risk: bool
    narrative: List[str]

class Patient(BaseModel):
    patient_id: str
    display_name: str
    year_of_birth: int
    living_setting: str
    programme: str
    clinical_focus: str

class PatientEvent(BaseModel):
    id: str
    patient_id: str
    timestamp: datetime
    type: str
    details: dict
    activity: Optional[ActivityState] = None
    fall: Optional[FallDetectionResult] = None

class IntakeRequest(BaseModel):
    organisationType: str
    organisationName: str
    contactName: str
    email: str
    region: str
    sizeBand: Optional[str] = ""
    notes: Optional[str] = ""

class IntakeResponse(BaseModel):
    ok: bool = True
    message: str

class RiskScoreInput(BaseModel):
    gaitVelocity: float = Field(ge=0, le=3)
    timeToStand: float = Field(ge=0, le=60)
    nighttimeBathroomVisits: int = Field(ge=0, le=20)
    recentFallsCount: int = Field(ge=0, le=10)
    age: int = Field(ge=40, le=110)
    frailtyIndex: Optional[float] = Field(default=None, ge=0, le=1)

class RiskScoreResult(BaseModel):
    riskScore: float
    band: str
    explanation: List[str]
    recommendations: List[str]

class TwinMetrics(BaseModel):
    timestamp: str
    gaitVelocity: float
    timeToStand: float
    fallRiskScore: float
    status: str

# --- DATA STORE ---
PATIENTS = [
    Patient(patient_id="HKLX-01", display_name="Mr A. Thompson", year_of_birth=1942, living_setting="Sheltered housing", programme="Bridging", clinical_focus="Sleep monitoring"),
    Patient(patient_id="HKLX-09", display_name="Mrs L. Bennett", year_of_birth=1950, living_setting="Own home", programme="Falls prevention", clinical_focus="Gait analysis"),
    Patient(patient_id="HKLX-04", display_name="Ms R. Collins", year_of_birth=1938, living_setting="Extra-care", programme="Dementia pathway", clinical_focus="Wandering risk"),
    Patient(patient_id="PAT_FALL", display_name="Mr J. Okoro", year_of_birth=1948, living_setting="Ground-floor flat", programme="Reablement", clinical_focus="Recurrent falls"),
    Patient(patient_id="PAT_BEND", display_name="Mrs P. Singh", year_of_birth=1955, living_setting="Own home", programme="Falls prevention", clinical_focus="Near-fall posture"),
    Patient(patient_id="PAT_OUT", display_name="Mr D. Hughes", year_of_birth=1946, living_setting="Retirement village", programme="Frailty", clinical_focus="Out-of-home patterns"),
    Patient(patient_id="PAT_VW01", display_name="Ms E. Garcia", year_of_birth=1952, living_setting="Home", programme="Virtual ward (COPD)", clinical_focus="Nocturnal activity"),
    Patient(patient_id="PAT_VW02", display_name="Mr K. Mensah", year_of_birth=1960, living_setting="Home", programme="Virtual ward (HF)", clinical_focus="Decompensation tracking"),
]
_EVENTS = deque(maxlen=5000)

# --- ADVANCED LOGIC (From hakilix_single.py) ---

def compute_risk_score(payload: RiskScoreInput) -> RiskScoreResult:
    score = 0.0
    explanation = []
    recs = []

    if payload.gaitVelocity < 0.6:
        score += 25
        explanation.append("Slow gait velocity associated with higher falls risk.")
    elif payload.gaitVelocity < 1.0:
        score += 10

    if payload.timeToStand > 20:
        score += 20
        explanation.append("Prolonged time to stand suggests deconditioning.")
    
    score += min(payload.recentFallsCount * 10, 30)
    if payload.age >= 85: score += 15
    elif payload.age >= 75: score += 10

    if score >= 70: band = "HIGH"
    elif score >= 40: band = "MEDIUM"
    else: band = "LOW"

    return RiskScoreResult(riskScore=score, band=band, explanation=explanation, recommendations=recs)

def detect_fall_logic(frames: List[SensorFrame]) -> FallDetectionResult:
    peak_g = max((abs(f.vertical_accel_g) for f in frames), default=0.0)
    is_fall = False
    severity = "LOW"
    conf = 0.0
    reasons = []

    if peak_g > 2.5:
        is_fall = True
        reasons.append(f"High-G impact detected: {peak_g:.2f}g")
        if peak_g > 3.5:
            severity = "HIGH"
            conf = 0.95
        else:
            severity = "MEDIUM"
            conf = 0.8

    return FallDetectionResult(is_fall=is_fall, confidence=conf, severity=severity, reason=reasons, flag_virtual_ward_review=is_fall)

def classify_activity(frames: List[SensorFrame]) -> ActivityState:
    avg_energy = mean(f.movement_energy for f in frames) if frames else 0.0
    label = "unknown"
    narrative = []
    
    if avg_energy < 0.05: label = "sleeping" if frames[-1].is_in_bed else "idle"
    elif avg_energy > 0.3: label = "walking"
    else: label = "active"
    
    return ActivityState(timestamp=datetime.utcnow(), label=label, confidence=0.7, is_potential_risk=False, narrative=narrative)

def generate_twin_metrics() -> TwinMetrics:
    now = datetime.utcnow().isoformat() + "Z"
    gait = 0.95
    tts = 8.5
    risk = compute_risk_score(RiskScoreInput(gaitVelocity=gait, timeToStand=tts, nighttimeBathroomVisits=1, recentFallsCount=0, age=80, frailtyIndex=0.25))
    status = "STABLE" if risk.band in ("LOW", "MEDIUM") else "HIGH_RISK"
    return TwinMetrics(timestamp=now, gaitVelocity=gait, timeToStand=tts, fallRiskScore=risk.riskScore, status=status)

# --- ENDPOINTS ---

@app.get("/", response_class=HTMLResponse)
async def read_root():
    try:
        path = os.path.join(os.path.dirname(__file__), "../web/index.html")
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except: return "<h1>Web Interface Missing</h1>"

@app.get("/api/patients", response_model=List[Patient])
def get_patients(): return PATIENTS

@app.post("/api/patients", response_model=Patient)
def create_patient(patient: Patient):
    if any(p.patient_id == patient.patient_id for p in PATIENTS): raise HTTPException(status_code=400, detail="Exists")
    PATIENTS.append(patient)
    return patient

@app.put("/api/patients/{patient_id}", response_model=Patient)
def update_patient(patient_id: str, patient: Patient):
    for i, p in enumerate(PATIENTS):
        if p.patient_id == patient_id:
            PATIENTS[i] = patient
            return patient
    raise HTTPException(status_code=404, detail="Not found")

@app.delete("/api/patients/{patient_id}")
def delete_patient(patient_id: str):
    global PATIENTS
    PATIENTS = [p for p in PATIENTS if p.patient_id != patient_id]
    return {"status": "deleted"}

@app.post("/api/intake", response_model=IntakeResponse)
def api_intake(payload: IntakeRequest):
    return IntakeResponse(ok=True, message=f"Received application from {payload.organisationName}")

@app.post("/api/risk-score", response_model=RiskScoreResult)
def api_risk_score(payload: RiskScoreInput):
    return compute_risk_score(payload)

@app.get("/api/twin-metrics", response_model=TwinMetrics)
def api_twin_metrics():
    return generate_twin_metrics()

@app.post("/api/ingest", response_model=PatientEvent)
async def ingest_telemetry(payload: SensorWindow):
    fall_result = detect_fall_logic(payload.frames)
    activity_result = classify_activity(payload.frames)
    
    event_type = "TELEMETRY"
    if fall_result.is_fall:
        event_type = "CRITICAL_FALL"
        logger.critical(f"[ALERT] {payload.patient_id} FALL DETECTED")

    event = PatientEvent(
        id=str(uuid.uuid4()),
        patient_id=payload.patient_id,
        timestamp=datetime.now(),
        type=event_type,
        details=fall_result.dict(),
        activity=activity_result,
        fall=fall_result
    )
    _EVENTS.append(event)
    return event

@app.get("/api/events")
async def get_events(limit: int = 100):
    return list(reversed(list(_EVENTS)))[:limit]

# --- WEBSOCKETS ---
from fastapi import WebSocket, WebSocketDisconnect
class ConnectionManager:
    def __init__(self): self.active_connections = []
    async def connect(self, websocket: WebSocket): await websocket.accept(); self.active_connections.append(websocket)
    def disconnect(self, websocket: WebSocket): self.active_connections.remove(websocket)
    async def broadcast(self, message: str):
        for connection in self.active_connections: await connection.send_text(message)

manager = ConnectionManager()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True: await websocket.receive_text()
    except WebSocketDisconnect: manager.disconnect(websocket)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)