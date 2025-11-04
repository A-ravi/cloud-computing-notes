#!/usr/bin/python3

import boto3

sqs = boto3.client('sqs', region_name='us-east-1')

# Create a queue
response = sqs.create_queue(
    QueueName='my-standard-queue'
)
queue_url = response['QueueUrl']
print("Queue created:", queue_url)

# Create a FIFO queue
response = sqs.create_queue(
    QueueName='my-fifo-queue.fifo',
    Attributes={
        'FifoQueue': 'true',
        'ContentBasedDeduplication': 'true'
    }
)
fifo_queue_url = response['QueueUrl']
print("FIFO queue created:", queue_url)


# send message to queue
sqs.send_message(
    QueueUrl=queue_url,
    MessageBody='Hello from SQS!',
    MessageAttributes={
        'Author': {
            'DataType': 'String',
            'StringValue': 'Ravi'
        }
    }
)
print("Message sent!")

# send message to FIFO queue
sqs.send_message(
    QueueUrl=fifo_queue_url,
    MessageBody='Order #123 Created',
    MessageGroupId='order-processing-group'
)


# Receive and Delete message after  processing

response = sqs.receive_message(
    QueueUrl=queue_url,
    MaxNumberOfMessages=2,   # up to 10 at once
    WaitTimeSeconds=10       # long polling
)

messages = response.get('Messages', [])
for msg in messages:
    print(f"Message: {msg['Body']}  |  ReceiptHandle: {msg['ReceiptHandle']}")
    
    sqs.delete_message(
        QueueUrl=queue_url,
        ReceiptHandle=msg['ReceiptHandle']
    )
    print("Deleted message:", msg['MessageId'])

# Visibility Timeout
# When a consumer reads a message, it becomes invisible for a certain time (default 30 sec).
# If the consumer fails to delete it before timeout → message becomes visible again.
# This avoids message loss if processing fails.
# You can change it per queue:

sqs.set_queue_attributes(
    QueueUrl=queue_url,
    Attributes={'VisibilityTimeout': '60'}
)

sqs.delete_queue(QueueUrl=queue_url)
print("Queue deleted!")

sqs.delete_queue(QueueUrl=fifo_queue_url)
print("Queue deleted!")
