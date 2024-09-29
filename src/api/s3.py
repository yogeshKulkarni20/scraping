import boto3
import os
from dotenv import load_dotenv
from src.utils.logging_utils import logger
from src.constant import s3_comments_data_bucket

# Load environment variables
load_dotenv()

# AWS credentials and S3 setup
s3_client = boto3.client(
    's3',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name=os.getenv('AWS_REGION')
)


def upload_file_to_s3(file_path, s3_file_path):
    try:
        logger.info(
            f"Uploading {file_path} to s3://{s3_comments_data_bucket}/{s3_file_path}")
        s3_client.upload_file(file_path, s3_comments_data_bucket, s3_file_path)
        logger.info(f"Uploaded {file_path} successfully to S3.")
    except Exception as e:
        logger.error(f"Error uploading {file_path}: {str(e)}")
