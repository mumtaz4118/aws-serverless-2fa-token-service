#!/bin/bash

# Set your AWS credentials  
export AWS_ACCESS_KEY_ID="AWS_ACCESS_KEY_ID"  
export AWS_SECRET_ACCESS_KEY="AWS_SECRET_ACCESS_KEY"  
export AWS_REGION="AWS_REGION"  

# Set your S3 bucket name which can be different as per the availability.  

BUCKET_NAME="aws-serverless-2fa-token-service\"

check_and_create_bucket() {  
  local bucket_name="$1"  
  if ! aws s3api head-bucket --bucket "$bucket_name" 2>/dev/null; then  
    echo "Bucket '$bucket_name' does not exist. Creating the bucket..."  
    aws s3api create-bucket --bucket "$bucket_name" --region "$AWS_REGION"  
    echo "Bucket '$bucket_name' created successfully."  
  fi  
}  

# Directories to zip  
dirs=(  
  "token_verification_lambda"  
  "token_creation_lambda"  
  "send_code_lambda"  
)  

# Loop through each directory  
for dir in "${dirs[@]}"; do  
  if [ -d "$dir" ]; then  
    # Create a zip file with the directory name
    zip_file_name="${dir}.zip"
    cd "$dir" || exit
    zip -r "../$zip_file_name" ./*
    cd ..

    echo "Created ZIP file: $zip_file_name"  
  else  
    echo "Error: Directory '$dir' not found."  
  fi  
done    

check_and_create_bucket "$BUCKET_NAME"  

# Check for ZIP files in the current directory  
find . -maxdepth 1 -name "*.zip" -print0 | while IFS= read -r -d $'\0' file; do  
  aws s3 cp "$file" "s3://$BUCKET_NAME/${file##*/}"  
  echo "Uploaded '$file' to S3 bucket '$BUCKET_NAME'."  

  base_name=$(basename "$file" ".zip")
  if [[ "${dirs[*]}" =~ "$base_name" ]]; then  
    rm "$file"   
    echo "Deleted '$file' locally."  
  else  
    echo "Skipping deletion for '$file' as its base name is not in the dirs array."  
  fi  
done  
