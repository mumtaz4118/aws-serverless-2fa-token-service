import json
import boto3
import time
import random
import jwt
import os
from datetime import datetime, timedelta

# Initialize resources
dynamodb = boto3.resource('dynamodb')
lambda_client = boto3.client('lambda')

# Get environment variables  
SEND_VERIFICATION_CODE_LAMBDA_ARN = os.environ.get('SendVerificationCodeLambdaArn')  
DYNAMODB_TABLE_NAME = os.environ.get('UserTokensTableName') 
SENDER_EMAIL = os.environ.get('SenderEmail')
SECRET_KEY = os.environ.get('SecretKeyJwtToken')

def invoke_email_lambda(sender_email, receiver_email, subject, body):
    """Invoke the email sending Lambda function."""
    payload = {
        'sender_email': sender_email,
        'receiver_email': receiver_email,
        'subject': subject,
        'body': body
    }

    response = lambda_client.invoke(
        FunctionName=SEND_VERIFICATION_CODE_LAMBDA_ARN,
        InvocationType='Event',  # Use 'RequestResponse' for synchronous execution, 'Event' for asynchronous
        Payload=json.dumps(payload)
    )

    return response

def lambda_handler(event, context):
    """Lambda function handler to create a token and send a verification code."""
    table = dynamodb.Table(DYNAMODB_TABLE_NAME)
    body = json.loads(event['body'])  

    # Extract email from the request body  
    email = body.get('email')
    if not email:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Email is required.'})
        }

    # Generate JWT token and verification code
    token = jwt.encode({'email': email, 'exp': datetime.utcnow() + timedelta(minutes=30)}, SECRET_KEY, algorithm='HS256')
    verification_code = random.randint(10000, 999999)

    # Save the token and verification code in DynamoDB
    table.put_item(
        Item={
            'email': email,
            'token': token,
            'expiration_time': int(time.time()) + 1800,
            'verification_code': verification_code
        }
    )

    # Prepare and send the verification email
    email_subject = "Verification Code"
    email_body = f"Your verification code is: {verification_code}"
    response = invoke_email_lambda(SENDER_EMAIL, email, email_subject, email_body)

    return {
        'statusCode': 200,
        'body': json.dumps({
            'message': 'Token created and saved in DynamoDB table "UserTokensTable".',
            'verification_code': verification_code
        })
    }
