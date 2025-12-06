import json
import boto3
import os
import time

# Mocking boto3 for local dev if not installed
try:
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ.get('TABLE_NAME', 'HakilixEvents'))
except:
    print("Warning: boto3 not configured")

def lambda_handler(event, context):
    print("Received Alert:", json.dumps(event))
    
    try:
        # Check if table exists before putting item
        if 'table' in globals():
            table.put_item(Item={
                'device_id': event['device_id'],
                'timestamp': int(time.time()),
                'alert_type': event['status'],
                'meta': event.get('meta', {})
            })
        return {'statusCode': 200, 'body': 'Alert Persisted'}
    except Exception as e:
        print(e)
        return {'statusCode': 500}