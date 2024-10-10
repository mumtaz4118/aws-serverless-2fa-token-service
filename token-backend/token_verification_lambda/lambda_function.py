import json
import jwt
import boto3
import time
from decimal import Decimal
from boto3.dynamodb.types import TypeDeserializer
import os

# Initialize DynamoDB resource
dynamodb = boto3.resource('dynamodb')
DYNAMODB_TABLE_NAME = os.environ.get('UserTokensTableName')
SECRET_KEY = os.environ.get('SecretKeyJwtToken')

# Access the DynamoDB table
table = dynamodb.Table(DYNAMODB_TABLE_NAME)
deserializer = TypeDeserializer()

def get_verification_code_item(verification_code):
    """Retrieve an item from DynamoDB using the verification code."""
    response = table.scan(
        FilterExpression='verification_code = :vc',
        ExpressionAttributeValues={':vc': verification_code}
    )
    return response['Items'][0] if response['Items'] else None

def deserialize_item(item):
    """Convert DynamoDB item to a more usable format."""
    email = item['email']
    token = item['token']
    expiration_time = deserializer.deserialize({'N': str(item['expiration_time'])})
    return email, token, expiration_time

def decode_token(token):
    """Decode the JWT token and return the email or error message."""
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return decoded_token['email'], None
    except jwt.ExpiredSignatureError:
        return None, 'Token has expired'
    except jwt.InvalidTokenError:
        return None, 'Invalid token'

def verify_token_email(token_email, item_email):
    """Check if the token email matches the item email."""
    return token_email == item_email

def is_token_expired(expiration_time):
    """Check if the token is expired based on the current time."""
    return int(time.time()) > expiration_time

def response(status_code, message):
    """Format the response for the Lambda function."""
    return {
        'statusCode': status_code,
        'body': json.dumps(message)
    }

def lambda_handler(event, context):
    """Main Lambda function handler to verify the token using the verification code."""
    body = json.loads(event['body'])
    
    # Validate the presence of verification_code
    verification_code = body.get('verification_code')
    if verification_code is None:
        return response(400, 'Verification code is required.')

    # Retrieve item from DynamoDB
    item = get_verification_code_item(int(verification_code))
    if not item:
        return response(400, 'Invalid verification code')

    # Deserialize item
    email, token, expiration_time = deserialize_item(item)

    # Decode the token
    token_email, error_message = decode_token(token)
    if error_message:
        return response(400, error_message)

    # Verify email and expiration
    if not verify_token_email(token_email, email):
        return response(400, 'Email mismatch')

    if is_token_expired(expiration_time):
        return response(400, 'Token has expired')

    return response(200, {
        'email': email,
        'message': "Token verified successfully"
    })
