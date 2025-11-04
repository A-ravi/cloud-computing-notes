#!/usr/bin/python3
import botocore.session

# Create a botocore session
session = botocore.session.get_session()
sts_client = session.create_client('sts', region_name='us-east-1')

resp = sts_client.get_caller_identity()
print(resp)
