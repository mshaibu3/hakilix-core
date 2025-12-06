# HAKILIX CORE | Neuromorphic Edge AI Platform

![Status](https://img.shields.io/badge/Status-Alpha-orange) ![Python](https://img.shields.io/badge/Python-3.9%2B-blue) ![License](https://img.shields.io/badge/License-Proprietary-red)

**Principal Investigator:** Musah Shaibu  
**Institution:** Hakilix Labs UK  

## 1. Overview
Hakilix is a privacy-first ambient intelligence platform designed for the Ageing Society. It utilizes **Spiking Neural Networks (SNN)** and **Structural Causal Models (SCM)** to detect physiological anomalies (falls, gait deterioration) without optical cameras.

This repository contains the full stack implementation:
* **Edge Firmware:** Python 3.9 asyncio-based sensor fusion engine.
* **Neuromorphic Core:** Custom Leaky Integrate-and-Fire (LIF) implementation.
* **Cloud Infrastructure:** AWS Serverless backend (IoT Core, DynamoDB, Lambda).

## 2. Architecture
The system follows a distributed "Edge-Cloud Continuum" topology:

```
[ RADAR (mmWave) ] --(UART)--> [ EDGE NODE (Pi 4) ] --(MQTT/TLS)--> [ AWS IOT CORE ]
[ THERMAL (Lepton)] --(SPI)--> [ SNN INFERENCE  ]                 [ DYNAMODB ]
                               [ FUSION ENGINE  ]
```

## 3. Quick Start (Simulation Mode)
The codebase includes a hardware abstraction layer (HAL) that simulates sensor data if physical hardware is not detected.

```bash
# 1. Clone Repo
git clone [https://github.com/hakilix-labs/hakilix-core.git](https://github.com/hakilix-labs/hakilix-core.git)
cd hakilix-core

# 2. Install Dependencies (Virtual Env recommended)
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 3. Run the Edge Node
python3 -m edge.main
```

## 4. Hardware Requirements
* **Compute:** Raspberry Pi 4 Model B (4GB+) or NVIDIA Jetson Nano.
* **Radar:** Texas Instruments IWR6843ISK (60GHz FMCW).
* **Thermal:** FLIR Lepton 3.5 (Radiometric).

## 5. License
Copyright (c) 2025 Hakilix Labs UK Ltd. All Rights Reserved.
Strictly confidential. Do not distribute without written permission.