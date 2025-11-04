#!/usr/bin/python3

import boto3

# Two ways to interact
dynamodb_client = boto3.client('dynamodb', region_name='us-east-1')
dynamodb_resource = boto3.resource('dynamodb', region_name='us-east-1')


table_name = 'Users'

table = dynamodb_resource.create_table(
    TableName=table_name,
    KeySchema=[
        {'AttributeName': 'user_id', 'KeyType': 'HASH'}  # Partition key
    ],
    AttributeDefinitions=[
        {'AttributeName': 'user_id', 'AttributeType': 'S'}  # S=String
    ],
    BillingMode='PAY_PER_REQUEST'  # On-demand billing
)

print(f"✅ Creating table {table_name} ...")
table.wait_until_exists()
print("✅ Table created successfully!")


# List Tables
print("Listing tables")

for name in dynamodb_client.list_tables()['TableNames']:
    print(name)


# Put an Item to table
table = dynamodb_resource.Table('Users')

table.put_item(
    Item={
        'user_id': 'u123',
        'name': 'Ravi',
        'age': 25,
        'city': 'Mumbai'
    }
)

print("✅ Item inserted successfully!")

# Read an Item from table
response = table.get_item(Key={'user_id': 'u123'})

if 'Item' in response:
    print("🔍 Retrieved item:", response['Item'])
else:
    print("❌ Item not found.")



# Update an Item
table.update_item(
    Key={'user_id': 'u123'},
    UpdateExpression="set age = :a, city = :c",
    ExpressionAttributeValues={
        ':a': 26,
        ':c': 'Pune'
    },
    ReturnValues="UPDATED_NEW"
)
print("✅ Item updated!")



# Query with the primary key
response = table.query(
    KeyConditionExpression=boto3.dynamodb.conditions.Key('user_id').eq('u123')
)
for item in response['Items']:
    print(item)


# Scan the whole table
response = table.scan()
for item in response['Items']:
    print(item)


# Filter expersions
from boto3.dynamodb.conditions import Attr

response = table.scan(
    FilterExpression=Attr('age').gt(25)
)
for item in response['Items']:
    print(item)


# Delete Item
table.delete_item(Key={'user_id': 'u123'})
print("🧹 Item deleted!")



# Delete the table
table = dynamodb_resource.Table('Users')
table.delete()
table.wait_until_not_exists()
print("🧹 Table deleted successfully!")

















