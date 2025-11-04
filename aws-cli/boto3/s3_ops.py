import boto3

# Create both interfaces
s3_client = boto3.client('s3')
s3_resource = boto3.resource('s3')

# Create bucket (region-specific)
bucket_name = 'my-boto3-demo-bucket-4-11-2025'
s3_client.create_bucket(
    Bucket=bucket_name,
    CreateBucketConfiguration={'LocationConstraint': 'us-west-2'}
)

print("------------------- Listing all buckets -------------------")
# List all buckets using client
response = s3_client.list_buckets()
for b in response['Buckets']:
    print(b['Name'])

print("------------------- Listing all buckets -------------------")
# List all buckets using resource
for bucket in s3_resource.buckets.all():
    print(bucket.name)

# Upload using client
s3_client.upload_file('local.txt', bucket_name, 'remote.txt')

# Upload using resource
bucket = s3_resource.Bucket(bucket_name)
bucket.upload_file('local.txt', 'remote2.txt')

print("------------------- File Content -------------------")
# Read file content directly
obj = s3_client.get_object(Bucket=bucket_name, Key='remote.txt')
data = obj['Body'].read().decode('utf-8')
print(data)


print("------------------- Check if bucket exists -------------------")
# Check if the bucket exists
from botocore.exceptions import ClientError

def check_bucket_exists(bucket_name):
    try:
        s3_client.head_bucket(Bucket=bucket_name)
        return True
    except ClientError:
        return False

print(check_bucket_exists(bucket_name))

print("------------------- Bucket Metadata -------------------")

# Get Metadata of the bucket
response = s3_client.head_object(Bucket=bucket_name, Key='remote.txt')
print(response['ContentLength'], response['ContentType'])

# Tagging the objects
s3_client.put_object_tagging(
    Bucket=bucket_name,
    Key='remote.txt',
    Tagging={'TagSet': [{'Key': 'env', 'Value': 'test'}]}
)

## upload files have two method
# upload_file -> uploads the file on the filesystem
# uploadfileobj -> uploads the file from the stream/memory

## download file also have two method
# download_file
# download_fileobj

