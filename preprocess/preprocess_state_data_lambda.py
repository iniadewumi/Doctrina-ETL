
import os
import pandas as pd
from smart_open import open
import requests

def handler(event, context):
    try:
        bucket = event['bucket']
        state = event['state']
        
        preprocess_and_partition(bucket, state)
    except Exception as e:
        error_message = f"Error occurred in preprocess_state_data_lambda for state {state}: {str(e)}"
        send_slack_notification(error_message)
        raise

def preprocess_and_partition(bucket, state):
    input_file = f"s3://{bucket}/nppes/year=${now.year}/month=${now.month:02d}/NPPES_Data_Dissemination_${now.strftime('%B')}_${now.year}.zip"
    
    # Read the CSV file in chunks
    chunksize = 100000
    
    for chunk in pd.read_csv(open(input_file), chunksize=chunksize, low_memory=False):
        # Perform data preprocessing on the chunk
        chunk = chunk.dropna(subset=['NPI', 'Entity Type Code', 'Provider First Name', 'Provider Last Name', 'Provider Business Practice Location Address State Name'])
        
        # Filter the chunk by state
        state_chunk = chunk[chunk['Provider Business Practice Location Address State Name'] == state]
        
        # Partition the chunk by entity type
        entity_types = state_chunk['Entity Type Code'].unique()
        
        for entity_type in entity_types:
            entity_chunk = state_chunk[state_chunk['Entity Type Code'] == entity_type]
            
            # Save the partitioned chunk to S3
            output_file = f"s3://{bucket}/nppes/year=${now.year}/month=${now.month:02d}/entity_type={entity_type}/state={state}/NPPES_Data_Dissemination_${now.strftime('%B')}_${now.year}.csv"
            entity_chunk.to_csv(open(output_file, 'a'), index=False, header=False)
    
    print(f"Data preprocessing and partitioning completed for state: {state}")

def send_slack_notification(message):
    slack_webhook_url = os.environ['SLACK_WEBHOOK_URL']
    
    payload = {
        'text': message
    }
    
    response = requests.post(slack_webhook_url, json=payload)
    
    if response.status_code != 200:
        print(f"Failed to send Slack notification. Status code: {response.status_code}")
