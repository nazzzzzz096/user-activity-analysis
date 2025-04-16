import boto3

def lambda_handler(event, context):
    glue = boto3.client('glue')
    response = glue.start_job_run(JobName='etl-user-activity')
    return {
        'statusCode': 200,
        'body': 'Glue job started'
    }
