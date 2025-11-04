#!/usr/bin/python3

import boto3

iam_client = boto3.client("iam")

paginator = iam_client.get_paginator("list_roles")
aws_roles=[]

for page in paginator.paginate():
    for role in page["Roles"]:
        aws_roles.append(role["RoleName"])

print('\n'.join(aws_roles))

'''
How a Paginator works internally?
You call a client.get_paginator('operation_name').
It returns a Paginator object for that API call.
You call .paginate(**parameters) on it.
The paginator:
    Sends the request
    Reads the response
    Checks for a pagination token (e.g., NextToken, Marker)
    Makes the next call automatically until all pages are fetched.

Not every AWS API needs a paginator — only “list” or “describe” calls that can return more data than one page.


'''