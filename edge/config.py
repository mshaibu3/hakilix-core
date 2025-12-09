from pydantic import Field
from pydantic_settings import BaseSettings
class Settings(BaseSettings):
    DEVICE_ID: str = Field(default="HKLX-EDGE-001")
    MQTT_BROKER: str = "iot.eu-west-2.amazonaws.com"
config = Settings()