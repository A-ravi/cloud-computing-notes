#!/usr/bin/python3

import boto3
ssm_client = boto3.client('ssm', region_name='us-east-1')

ssm_client.put_parameter(
    Name='/app/config/db_name',
    Value='usersdb',
    Type='String',
    Overwrite=True
)
print("✅ Parameter created: /app/config/db_name")


ssm_client.put_parameter(
    Name='/app/secure/db_password',
    Value='SuperSecret@123',
    Type='SecureString',
    KeyId='alias/aws/ssm',  # Default AWS-managed KMS key
    Overwrite=True
)
print("🔐 Secure parameter stored.")

# get a parameter
response = ssm_client.get_parameter(Name='/app/config/db_name')
print("🧩 Value:", response['Parameter']['Value'])

# get a secure parameter
response = ssm_client.get_parameter(
    Name='/app/secure/db_password',
    WithDecryption=True
)
print("🔓 Decrypted value:", response['Parameter']['Value'])

# get multiple parameter
response = ssm_client.get_parameters(
    Names=['/app/config/db_name', '/app/secure/db_password'],
    WithDecryption=True
)

for param in response['Parameters']:
    print(f"{param['Name']} = {param['Value']}")


# Retrieve all under a folder path
response = ssm_client.get_parameters_by_path(
    Path='/app/dev/',
    Recursive=True,
    WithDecryption=True
)

for param in response['Parameters']:
    print(param['Name'], '=', param['Value'])

# update a parameter value
ssm_client.put_parameter(
    Name='/app/config/db_name',
    Value='usersdb_v2',
    Type='String',
    Overwrite=True
)
print("✅ Updated parameter value.")

# List All parameters
response = ssm_client.describe_parameters()
for param in response['Parameters']:
    print(param['Name'], '-', param['Type'])



# Delete a parameter
ssm_client.delete_parameter(Name='/app/config/db_name')
print("🧹 Parameter deleted.")


# Delete Multiple parameter
ssm_client.delete_parameters(
    Names=['/app/config/db_name', '/app/secure/db_password']
)
print("🧹 Deleted multiple parameters.")

'''
| Operation       | Boto3 Method               | Description                     |
| --------------- | -------------------------- | ------------------------------- |
| Create/Update   | `put_parameter()`          | Create or overwrite a parameter |
| Get One         | `get_parameter()`          | Retrieve a single parameter     |
| Get Many        | `get_parameters()`         | Get multiple by name            |
| Get By Path     | `get_parameters_by_path()` | Retrieve all under a prefix     |
| Delete          | `delete_parameter()`       | Remove a parameter              |
| Describe        | `describe_parameters()`    | List all with filters           |
| Version History | `get_parameter_history()`  | View older versions             |

'''