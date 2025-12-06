import os
from pydantic import Field
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # --- Device Identity ---
    DEVICE_ID: str = Field(default="HKLX-EDGE-001", env="DEVICE_ID")
    ENV: str = Field(default="development", env="ENV")
    
    # --- Cloud Connectivity ---
    MQTT_BROKER: str = Field(default="iot.eu-west-2.amazonaws.com", env="MQTT_BROKER")
    MQTT_PORT: int = 8883
    
    # --- Hardware Config ---
    # Set to False only when deploying to physical Pi
    SIMULATE_SENSORS: bool = Field(default=True, env="SIMULATE_SENSORS")
    RADAR_PORT: str = "/dev/ttyUSB0"
    RADAR_BAUD: int = 921600
    
    # --- Neuromorphic Hyperparameters (LIF Model) ---
    LIF_THRESHOLD: float = 1.0      # Membrane potential threshold
    LIF_DECAY: float = 0.95         # Membrane decay factor (tau)
    LIF_REST: float = 0.0           # Resting potential
    
    # --- Fusion Logic ---
    FALL_VELOCITY_LIMIT: float = 2.5  # m/s
    THERMAL_CONFIDENCE_MIN: float = 0.85

    class Config:
        env_file = ".env"

config = Settings()