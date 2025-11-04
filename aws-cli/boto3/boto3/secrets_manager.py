#!/usr/bin/python

# create a secret in secret manager
import boto3
import json

client = boto3.client('secretsmanager', region_name='us-east-1')

secret_name = "myapp/db_credentials"
secret_value = {
    "username": "admin",
    "password": "SuperStrong@123"
}

response = client.create_secret(
    Name=secret_name,
    Description="Database credentials for MyApp",
    SecretString=json.dumps(secret_value)
)

print(f"✅ Secret created: {response['ARN']}")

print("Print all secrets")
paginator = client.get_paginator('list_secrets')
for page in paginator.paginate():
    for secret in page['SecretList']:
        print(secret['Name'])


def get_secret(secret_name, region='us-east-1'):
    client = boto3.client('secretsmanager', region_name=region)
    response = client.get_secret_value(SecretId=secret_name)
    
    # The actual secret string is JSON text
    secret = json.loads(response['SecretString'])
    return secret

# Example
secret = get_secret("myapp/db_credentials")
print(secret["username"], secret["password"])

client.put_secret_value(
    SecretId="myapp/db_credentials",
    SecretString=json.dumps({
        "username": "admin",
        "password": "NewSecurePass@456"
    })
)
print("🔄 Secret updated successfully!")


client.delete_secret(
    SecretId="myapp/db_credentials",
    RecoveryWindowInDays=7,  # Optional (default 30)
    ForceDeleteWithoutRecovery=False
)
print("🧹 Secret scheduled for deletion.")

######################################################


region = 'us-east-1'
secret_name = 'demo/credentials'

client = boto3.client('secretsmanager', region_name=region)

# 1. Create secret
secret = {"user": "ravi", "pass": "Test@123"}
client.create_secret(Name=secret_name, SecretString=json.dumps(secret))
print("✅ Created secret")

# 2. Read it
resp = client.get_secret_value(SecretId=secret_name)
print("🔐 Secret:", resp['SecretString'])

# 3. Update
new_secret = {"user": "ravi", "pass": "Updated@456"}
client.put_secret_value(SecretId=secret_name, SecretString=json.dumps(new_secret))
print("🔄 Updated secret")

# 4. Delete
client.delete_secret(SecretId=secret_name, ForceDeleteWithoutRecovery=True)
print("🧹 Deleted secret")

