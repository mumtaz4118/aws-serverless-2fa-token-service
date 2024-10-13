# AWS Serverless 2FA Token Service

This is proof of concept implementation for a serverless backend system designed to generate and deliver single-use tokens for two-factor authentication (2FA). Built entirely on AWS, this solution emphasizes simplicity, security, and usability while ensuring resilience and modularity.

## Key Features:  
- **Serverless Architecture**: Utilizes AWS Lambda, API Gateway, and other serverless services to minimize costs and complexity while maintaining scalability.  
- **Token Generation**: Implements a secure mechanism for generating single-use tokens for 2FA workflows.  
- **Delivery Method**: Offers flexible options for token delivery (e.g., email, SMS) based on user preferences.  
- **Resilience**: Designed to handle failures gracefully, ensuring high availability and reliability of the service.  
- **Modular Design**: Components are decoupled to facilitate easier maintenance and future enhancements.  

## Bonus Implementation:
- Architecture diagram providing a visual representation of the system design.  
- Code excerpts and configuration details illustrating implementation choices.  
- Health, availability, and performance metrics for monitoring and optimization.  
- Security best practices to protect user data and token integrity.

## Steps towrds the deployment of the solution:

1. **Cloning Repository:**
	- Clone the guthub repository (containing the solutions) at your local machine by running the following commands.
	```
	git clone https://github.com/mumtaz4118/aws-serverless-2fa-token-service.git
	cd aws-serverless-2fa-token-service
	```
2. **Uploading the Lambda Functions' zips to S:3**
    - To upload the Lambda function ZIP files and the JWT Python library ZIP to the S3 bucket, execute the upload_files_to_s3.sh script. This script will generate the required ZIP files and upload them to the specified S3 bucket. Before running the script, ensure that you update your secret key, private key, and region within the file. Run the following command: 
    ```
    ./upload_files_to_s3.sh
    ```
3. **Deploy Infrastructure Using AWS Console**
    - Access the AWS Management Console and navigate to the **CloudFormation** service.
    - Click on **Create stack** and select **With new resources (standard)**.  
    - Upload the `aws-serverless-2fa-token-service.yaml` CloudFormation template.  
    - Provide the required parameters, including:  
        - **Region**  
        - **AccountId**  
        - **EnvironmentName**  
        - **UserTokensTableName**  
        - **SenderEmail**  
        - **SecretKeyJwtToken**  
        - **S3BucketName**  
    - Continue with the stack creation by following the on-screen step by step instructions.  
    - Upon completion of the stack creation, the infrastructure components, including the DynamoDB table, Lambda functions, and API Gateway, will be successfully deployed.
4. **Testing**
    - Once the stack creation is complete, you can copy the output variable value `TokenCreationAPIURL`. Use this URL to make a request via Postman, providing a JSON object in the body, formatted as: `{"email": "emailAddress"}`.
    - This request will send a token to the specified email address as well as return it in the API response for testing purposes.
    - To verify the token, locate the `TokenVerificationAPIURL` in the outputs and use it to call the `tokenVerification` API. Provide the verification code in the body as: `{"verification_code": "code"}`.
    - This will either validate the token or return an error based on the token's value.


## Important:  
1. Verify that both the sender and recipient email addresses used for verification code emails are confirmed in the Amazon SES console under the "Email Addresses" section.
2. Ensure that you have the required AWS credentials configured on your local machine prior to executing any scripts or CloudFormation commands.
3. Replace placeholders such as `<repository_url>`, `<stack_name>`, `<region>`, `<account_id>`, `<environment>`, `<table_name>`, `<sender_email>`, `<jwt_secret>`, and `<s3_bucket_name>` with your actual values before proceeding.
