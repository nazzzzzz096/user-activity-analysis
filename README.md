# user-activity-analysis
This is a cloud-based analysis I have done on the AWS platform. In this project, I shared a sample data to work on.

Steps to Set Up and Run the Pipeline
1. Create S3 Buckets
Create two folders in an S3 bucket (or separate buckets):

s3://user-activity-logs-naz/raw/ → for raw nested JSON input

s3://user-activity-logs-naz/processed/ → for transformed CSV output

2.Create an IAM Role for Glue
Create an IAM role named AWSGlueServiceRole-ETL with the following permissions:

json
Copy
Edit
{
  "Effect": "Allow",
  "Action": [
    "s3:GetObject",
    "s3:PutObject",
    "s3:ListBucket",
    "redshift:*"
  ],
  "Resource": [
    "arn:aws:s3:::user-activity-logs-naz",
    "arn:aws:s3:::user-activity-logs-naz/*"
  ]
}


3. Upload Glue Script
Upload glue_script.py to AWS Glue Studio or manually create a new job with the script.

Language: Python (Glue version 3.0+ recommended)

IAM Role: AWSGlueServiceRole-ETL

Temporary directory: e.g., s3://user-activity-logs-naz/temp/


4. Run the Glue Job
Go to AWS Glue > Jobs

Select your ETL job

Click Run Job

Monitor logs in CloudWatch if any errors occur

5. Output in S3
The cleaned and flattened CSV will be stored at:

arduino
Copy
Edit
s3://user-activity-logs-naz/processed/

6. Load to Amazon Redshift
You can copy the processed data into Redshift using SQL like:

sql
Copy
Edit
COPY user_action_summary
FROM 's3://user-activity-logs-naz/processed/'
IAM_ROLE 'arn:aws:iam::YOUR_ACCOUNT_ID:role/AWSGlueServiceRole-ETL'
FORMAT AS CSV
IGNOREHEADER 1;
