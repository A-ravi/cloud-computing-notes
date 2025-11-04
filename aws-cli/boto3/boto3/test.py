#!/usr/bin/python3

import boto3
import json

client = boto3.client("sts")
response = client.get_caller_identity()

print(json.dumps(response, indent=4))