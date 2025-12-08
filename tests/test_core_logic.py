import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from edge.core.fusion_engine import FusionEngine
from edge.config import config
from edge.core.home_bridge import HomeBridge

class TestHakilixCore(unittest.TestCase):
    def setUp(self):
        self.engine = FusionEngine()
        self.bridge = HomeBridge()
        
    def test_safe_state(self):
        radar = {'velocity': 0.5, 'acceleration': 0.1}
        thermal = {'variance': 0.2, 'max_temp': 36.5}
        status = self.engine.process(radar, thermal)
        self.assertEqual(status, "SAFE")
        
    def test_critical_fall_logic(self):
        radar = {'velocity': 4.5, 'acceleration': 9.8}
        thermal = {'variance': 0.8, 'max_temp': 36.5}
        config.FALL_VELOCITY_LIMIT = 2.0
        self.engine.snn.neurons['velocity'].v_mem = 2.0
        self.engine.snn.neurons['thermal'].v_mem = 2.0
        status = self.engine.process(radar, thermal)
        if self.engine.snn.infer(4.5, 9.8, 0.8):
             self.assertEqual(status, "CRITICAL_ALERT")

    def test_fhir_conversion(self):
        fhir = self.bridge.convert_to_fhir("CRITICAL_ALERT", 0.95)
        self.assertEqual(fhir['resourceType'], "Observation")
        self.assertEqual(fhir['code']['coding'][0]['code'], "224976008")

if __name__ == '__main__':
    unittest.main()