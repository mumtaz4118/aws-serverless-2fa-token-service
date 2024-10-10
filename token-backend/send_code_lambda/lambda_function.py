import json
import boto3
import os

# Configure the Amazon SES client using the environment variable for region
ses_client = boto3.client('ses', region_name=os.environ.get('Region'))

def send_email(sender_email, receiver_email, subject, body):
    """Sends an email using Amazon SES."""
    return ses_client.send_email(
        Destination={'ToAddresses': [receiver_email]},
        Message={
            'Body': {
                'Text': {
                    'Charset': 'UTF-8',
                    'Data': body,
                },
            },
            'Subject': {
                'Charset': 'UTF-8',
                'Data': subject,
            },
        },
        Source=sender_email
    )

def lambda_handler(event, context):
    """AWS Lambda handler to send an email using SES."""
    print("In email sending Lambda function")
    print(f"Event: {event}")

    sender_email = event.get('sender_email')
    receiver_email = event.get('receiver_email')
    subject = event.get('subject')
    body = event.get('body')

    # Send email and return response
    response = send_email(sender_email, receiver_email, subject, body)

    return {
        'statusCode': 200,
        'body': json.dumps({
            'message': 'Email sent successfully.',
            'message_id': response['MessageId']
        })
    }
