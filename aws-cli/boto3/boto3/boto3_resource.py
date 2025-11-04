#!/usr/bin/python3

import boto3

iam_resources = boto3.resource("iam")

aws_roles = []

for role in iam_resources.roles.all():
    aws_roles.append(role.name)

print("\n".join(aws_roles))