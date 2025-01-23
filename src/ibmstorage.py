import ibm_boto3
from ibm_botocore.client import Config, ClientError
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize COS client
cos_client = ibm_boto3.client(
    service_name='s3',
    ibm_api_key_id=os.getenv('IBM_COS_API_KEY_ID'),
    ibm_service_instance_id=os.getenv('IBM_COS_SERVICE_INSTANCE_ID'),
    config=Config(signature_version='oauth'),
    endpoint_url='https://s3.us-south.cloud-object-storage.appdomain.cloud' 
)


cos_client.upload_file('C:/Users/sharafM/Desktop/Ai_Try/watsonx/03_Discovery_chat/static/audio/2025-01-22_15-33-32_THARAKA.mp3', 
                       "bocbucketcoolzzzzzzzzzzz", 
                       '2025-01-22_15-33-32_THARAKA.mp3')

