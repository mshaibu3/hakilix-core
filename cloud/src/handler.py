import json
import boto3
import os
import time

try:
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ.get('TABLE_NAME', 'HakilixEvents'))
except:
    print("Warning: boto3 not configured")

def triage_event(event_type, confidence):
    """
    Hakilix Triage Logic (Red/Amber/Green)
    """
    confidence = float(confidence)
    if event_type == "CRITICAL_ALERT":
        if confidence > 0.90: return "RED"   # Ambulance
        elif confidence > 0.60: return "AMBER" # Nurse
    return "GREEN" # Log

def lambda_handler(event, context):
    print("Received Payload:", json.dumps(event))
    try:
        triage_status = triage_event(event.get('status'), event.get('confidence', 0.9))
        print(f"TRIAGE RESULT: {triage_status}")
        
        if 'table' in globals():
            table.put_item(Item={
                'device_id': event['device_id'],
                'timestamp': int(time.time()),
                'alert_type': event['status'],
                'triage_level': triage_status,
                'meta': event.get('meta', {})
            })
        return {'statusCode': 200, 'body': f'Triage: {triage_status}'}
    except Exception as e:
        print(e)
        return {'statusCode': 500}