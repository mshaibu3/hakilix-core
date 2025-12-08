# HAKILIX CORE | Neuromorphic Edge AI Platform

![Status](https://img.shields.io/badge/Status-Alpha-orange) ![Python](https://img.shields.io/badge/Python-3.9%2B-blue) ![License](https://img.shields.io/badge/License-Proprietary-red)

**Principal Investigator:** Musah Shaibu  
**Institution:** Hakilix Labs UK  

## 1. Overview
Hakilix is a privacy-first ambient intelligence platform designed for the Ageing Society. It utilizes **Spiking Neural Networks (SNN)** and **Structural Causal Models (SCM)** to detect physiological anomalies (falls, gait deterioration) without optical cameras.

## 2. Architecture
The system follows a distributed "Edge-Cloud Continuum" topology:

```
[ RADAR (mmWave) ] --(UART)--> [ EDGE NODE (Pi 4) ] --(MQTT/TLS)--> [ AWS IOT CORE ]
                                                                        |
[ THERMAL (Lepton)] --(SPI)--> [ SNN INFERENCE  ]                       v
                               [ HOME BRIDGE (FHIR) ]             [ CLOUD BACKEND ]
                                                                        |
                                                                        v
                                                               [ CAREGIVER DASHBOARD ]
```

## 3. Quick Start (Simulation Mode)

### A. Run the Edge Node (Sensor Simulation)
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 -m edge.main
```

### B. Launch the Caregiver Dashboard
Open `frontend/caregiver_dashboard.html` in your web browser. It will connect to the mock API and display live alerts.

## 4. License
Copyright (c) 2025 Hakilix Labs UK Ltd. All Rights Reserved.
Strictly confidential. Do not distribute without written permission.