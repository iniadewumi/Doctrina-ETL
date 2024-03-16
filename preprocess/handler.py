
import os, sys, time
import requests

sys.path.append(os.path.join(os.path.dirname(__file__)))

import download_file as download
import preprocess_data as preprocess

def handler(event, context):
    try:
        start_time = time.perf_counter()
        bucket = os.environ['DATA_BUCKET']
        action = event.get('action')
        if 'download' in action:
            download.run_download(event, bucket)

        # Preprocess the data and partition by entity type and state
        preprocess.preprocess_and_partition(bucket)
        
        end_time = time.perf_counter()
        print(f"Time elapsed is {end_time - start_time}")
    except:
        error_message = f"Error occurred in orchestrator_lambda: {str(e)}"
        send_slack_notification(error_message)
        raise

def send_slack_notification(message):
    slack_webhook_url = os.environ['SLACK_WEBHOOK_URL']
    payload = { 'text': message }
    response = requests.post(slack_webhook_url, json=payload)
    
    if response.status_code != 200:
        print(f"Failed to send Slack notification. Status code: {response.status_code}")