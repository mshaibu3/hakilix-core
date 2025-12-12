import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, BackgroundTasks, Header
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json, logging, os, sqlite3, asyncio
from datetime import datetime
from typing import List, Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Backend")

app = FastAPI(title="Hakilix Core Enterprise", version="18.0.0")

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# --- DATABASE ---
def init_db():
    conn = sqlite3.connect('hakilix.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS events (id INTEGER PRIMARY KEY, patient_id TEXT, type TEXT, details TEXT, timestamp TEXT)''')
    conn.commit()
    conn.close()

def persist_event(event_data):
    conn = sqlite3.connect('hakilix.db')
    conn.execute("INSERT INTO events (patient_id, type, details, timestamp) VALUES (?, ?, ?, ?)",
                 (event_data['patient_id'], event_data['type'], json.dumps(event_data['details']), event_data['timestamp']))
    conn.commit()
    conn.close()
    logger.info(f"[DB] Persisted event for {event_data['patient_id']}")

init_db()

# --- CONNECTION MANAGER ---
class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
    async def broadcast(self, message: str):
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except:
                self.disconnect(connection)

manager = ConnectionManager()

# --- MODELS ---
class SensorWindow(BaseModel):
    patient_id: str
    frames: list

class Patient(BaseModel):
    patient_id: str
    display_name: str
    year_of_birth: int
    living_setting: str
    programme: str
    clinical_focus: str

PATIENTS = [
    Patient(patient_id="HKLX-01", display_name="Mr A. Thompson", year_of_birth=1942, living_setting="Living Room", programme="Bridging", clinical_focus="Sleep monitoring"),
    Patient(patient_id="HKLX-09", display_name="Mrs L. Bennett", year_of_birth=1950, living_setting="Kitchen", programme="Falls prevention", clinical_focus="Gait analysis"),
    Patient(patient_id="HKLX-04", display_name="Ms R. Collins", year_of_birth=1938, living_setting="Bedroom", programme="Dementia pathway", clinical_focus="Wandering risk"),
]

# --- ENDPOINTS ---
@app.get("/", response_class=HTMLResponse)
async def read_root():
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        path_opt1 = os.path.join(current_dir, "../web/index.html")
        if os.path.exists(path_opt1):
            with open(path_opt1, "r", encoding="utf-8") as f: return f.read()
        return "<h1>Web Interface Missing</h1>"
    except Exception as e: return f"<h1>Error: {e}</h1>"

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

@app.post("/api/ingest")
async def ingest(payload: SensorWindow, background_tasks: BackgroundTasks, x_api_key: Optional[str] = Header(None)):
    # Simple Auth Check
    if x_api_key != "hakilix-secret-key-v1":
        logger.warning("Unauthenticated ingestion attempt.")
        # Allowing for demo, but normally raise 401
    
    frame = payload.frames[0]
    g_force = abs(frame.get('vertical_accel_g', 0))
    posture = frame.get('posture_angle_deg', 90)
    energy = frame.get('movement_energy', 0)
    zone = frame.get('zone', 'living_room')
    
    status = "Stable"
    evt_type = "TELEMETRY"
    
    if g_force > 3.0:
        status = "CRITICAL FALL"
        evt_type = "CRITICAL_FALL"
        logger.critical(f"FALL DETECTED: {payload.patient_id}")
    elif posture < 30: status = "Lying Down"
    elif posture > 70 and energy > 0.3: status = "Walking"
    elif posture > 70 and energy < 0.1: status = "Standing"
    elif 30 <= posture <= 70: status = "Seated"
    if energy > 0.8 and zone == "hallway": status = "Wandering (Confused)"

    event_data = {
        "patient_id": payload.patient_id,
        "type": evt_type,
        "timestamp": datetime.now().isoformat(),
        "details": {"peak_g": g_force, "status": status}
    }

    # Async Write
    background_tasks.add_task(persist_event, event_data)

    # Real-time Push
    await manager.broadcast(json.dumps(event_data))
    
    return {"status": "ok"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True: await websocket.receive_text()
    except WebSocketDisconnect: manager.disconnect(websocket)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8080)