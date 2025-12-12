import time, random, logging, requests
from datetime import datetime
from collections import deque

logging.basicConfig(level=logging.INFO, format='%(asctime)s | Hakilix.Edge | %(levelname)s | %(message)s')
BACKEND_URL = "http://127.0.0.1:8080/api/ingest"
DEVICE_ID = "HKLX-01" 
API_KEY = "hakilix-secret-key-v1"

# Offline Buffer
offline_queue = deque(maxlen=100)

def run():
    print("--- HAKILIX EDGE SENSOR ACTIVE (RESILIENT MODE) ---")
    states = ["Seated", "Walking", "Lying", "Wandering"]
    current_state = "Seated"
    state_timer = 0
    
    while True:
        # Simulate State
        state_timer += 1
        if state_timer > 10:
            current_state = random.choice(states)
            state_timer = 0
            print(f"[Behavior Change] Patient is now: {current_state}")

        accel = 0.98; posture = 90; energy = 0.0; zone = "living_room"
        
        if current_state == "Seated": posture = 45; energy = 0.05
        elif current_state == "Walking": posture = 85; energy = 0.4
        elif current_state == "Lying": posture = 10; energy = 0.01; zone = "bedroom"
        elif current_state == "Wandering": posture = 80; energy = 0.9; zone = "hallway"
        
        payload = {
            "patient_id": DEVICE_ID,
            "frames": [{
                "vertical_accel_g": accel,
                "posture_angle_deg": posture,
                "movement_energy": energy,
                "zone": zone
            }]
        }
        
        # Try sending
        try:
            # Check if we have buffered items
            while offline_queue:
                print(f"[RECOVERY] Flushing buffer... ({len(offline_queue)} items)")
                old_payload = offline_queue[0]
                requests.post(BACKEND_URL, json=old_payload, headers={"x-api-key": API_KEY}, timeout=1.0)
                offline_queue.popleft() # Remove if successful
            
            # Send current
            requests.post(BACKEND_URL, json=payload, headers={"x-api-key": API_KEY}, timeout=1.0)
            
        except Exception as e:
            print(f"[NETWORK ERROR] Backend unreachable. Buffering data... (Buffer size: {len(offline_queue)})")
            offline_queue.append(payload)
        
        time.sleep(1.0)

if __name__ == "__main__":
    try: run()
    except KeyboardInterrupt: print("\n[Edge] Shutting down.")