import json
import logging
import time

logger = logging.getLogger("Hakilix.HomeBridge")

class HomeBridge:
    def __init__(self):
        self.patient_id = "PAT-UK-8492"

    def convert_to_fhir(self, event_type, confidence):
        fhir_packet = {
            "resourceType": "Observation",
            "id": f"obs-{int(time.time())}",
            "status": "final",
            "code": {
                "coding": [{"system": "http://snomed.info/sct", "code": "224976008", "display": "Fall detected"}]
            },
            "subject": {"reference": f"Patient/{self.patient_id}"},
            "valueQuantity": {"value": confidence * 100, "unit": "%"}
        }
        logger.info("Converted Alert to HL7 FHIR Standard.")
        return fhir_packet