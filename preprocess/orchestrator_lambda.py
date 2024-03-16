# orchestrator_lambda.py

import os, sys, time
import boto3

sys.path.append(os.path.join(os.path.dirname(__file__)))

import download_file as download

def handler(event, context):
    try:
        start_time = time.perf_counter()
        bucket = os.environ['DATA_BUCKET']
        
        # Download the data
        download.run_download(event, bucket)
        
        # Trigger Lambda functions for each state
        states = get_states_from_s3(bucket)
        lambda_client = boto3.client('lambda')
        
        for state in states:
            payload = { 'bucket': bucket, 'state': state }
            lambda_client.invoke(FunctionName='preprocess_state_data', InvocationType='Event', Payload=json.dumps(payload))

        end_time = time.perf_counter()
        print(f"Time elapsed is {end_time - start_time}")
    except:
        error_message = f"Error occurred in orchestrator_lambda: {str(e)}"
        send_slack_notification(error_message)
        raise

def get_states_from_s3(bucket):
    s3_client = boto3.client('s3')
    prefix = f"nppes/year=${now.year}/month=${now.month:02d}/"
    
    response = s3_client.list_objects_v2(Bucket=bucket, Prefix=prefix, Delimiter='/')
    states = [obj['Prefix'].split('/')[-2] for obj in response.get('CommonPrefixes', [])]
    
    return states


def send_slack_notification(message):
    slack_webhook_url = os.environ['SLACK_WEBHOOK_URL']
    payload = {'text': message }    
    response = requests.post(slack_webhook_url, json=payload)
    
    if response.status_code != 200:
        print(f"Failed to send Slack notification. Status code: {response.status_code}")

