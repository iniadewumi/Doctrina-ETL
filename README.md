# Doctrina NPI ETL Pipeline

This repository contains an ETL (Extract, Transform, Load) pipeline designed for processing healthcare National Provider Identifier (NPI) data. The pipeline efficiently downloads, preprocesses, and partitions the data by entity type and state, facilitating further analysis and reporting.

## Architecture

The ETL pipeline includes the following components:

- **Orchestrator Lambda Function**: Serves as the entry point of the pipeline, responsible for downloading NPI data from the specified URL and triggering state-specific Lambda functions for parallel processing.
- **State-specific Lambda Functions**: Triggered by the Orchestrator Lambda for each state, these functions preprocess the data, partition it by entity type, and store the partitioned data in Amazon S3.
- **Amazon S3**: Stores the downloaded and preprocessed NPI data for further analysis and querying.

## Features

- Efficiently downloads large NPI data files from a specified URL.
- Preprocesses data to handle missing values and validate data integrity.
- Partitions data by entity type and state for optimized querying and analysis.
- Utilizes parallel processing for improved performance.
- Implements robust error handling with Slack notifications for monitoring and troubleshooting.
- Modular and extensible design for easy customization and integration.

## Prerequisites

Before running the ETL pipeline, ensure you have:

- An AWS account with permissions to manage Lambda functions, S3 buckets, and IAM roles.
- Python 3.x installed on your local machine.
- Required Python dependencies: `boto3`, `pandas`, `requests`, `smart_open`.
- A Slack webhook URL for error notifications.

## Setup and Deployment

1. Clone this repository to your local machine.
2. Set up an AWS account and create necessary IAM roles and permissions for Lambda functions and S3 access.
3. Create an S3 bucket for storing downloaded and preprocessed NPI data.
4. Update `orchestrator_lambda.py` and `preprocess_state_data_lambda.py` with appropriate AWS resource names (e.g., S3 bucket name, Lambda function names).
5. Set the `SLACK_WEBHOOK_URL` environment variable for both Lambda functions to your Slack webhook URL.
6. Package the Lambda functions and their dependencies into ZIP files.
7. Deploy the Lambda functions to AWS using the AWS Management Console or AWS CLI.
8. Test the ETL pipeline by triggering the Orchestrator Lambda with the appropriate event payload.

## Usage

To run the ETL pipeline, trigger the Orchestrator Lambda function with the following event payload:

```json
{
  "url": "https://download.cms.gov/nppes/NPPES_Data_Dissemination_${now_month_text}_${now_year}.zip",
  "output": "nppes/year=${now_year}/month=${now_month_02}/NPPES_Data_Dissemination_${now_month_text}_${now_year}.zip"
}
```

Replace the placeholders (${now_month_text}, ${now_year}, ${now_month_02}) with the appropriate values. The pipeline will then download the NPI data, preprocess it, partition it by entity type and state, and store the partitioned data in the specified S3 bucket.

Monitor the pipeline's progress and any errors through AWS CloudWatch logs and the configured Slack channel.