#!/usr/bin/python3

# test_assume_role.py
import boto3
import botocore
from datetime import datetime, timezone

def assume_role_and_create_session(role_arn, session_name="mysession", duration_seconds=3600, external_id=None):
    """
    Returns a boto3.Session object using temporary credentials from STS AssumeRole.
    """
    sts = boto3.client("sts")  # uses default credentials/credential provider chain
    assume_args = {
        "RoleArn": role_arn,
        "RoleSessionName": session_name,
        "DurationSeconds": duration_seconds,
    }
    if external_id:
        assume_args["ExternalId"] = external_id

    resp = sts.assume_role(**assume_args)
    creds = resp["Credentials"]

    # Create a session using temporary credentials
    session = boto3.Session(
        aws_access_key_id=creds["AccessKeyId"],
        aws_secret_access_key=creds["SecretAccessKey"],
        aws_session_token=creds["SessionToken"],
    )
    # optional: attach expiry to session object for debug/refresh logic
    session._assumed_role_expiration = creds["Expiration"]
    return session

if __name__ == "__main__":
    # Example usage
    ROLE_ARN = "arn:aws:iam::924515470898:role/LabRole"
    s = assume_role_and_create_session(ROLE_ARN, session_name="tooling-session", duration_seconds=3600)
    s3 = s.client("s3")
    # List buckets using the assumed role
    print("Using assumed role; Time:", datetime.now(timezone.utc).isoformat())
    try:
        for b in s3.list_buckets()["Buckets"]:
            print("-", b["Name"])
    except botocore.exceptions.ClientError as e:
        print("AWS error:", e)
