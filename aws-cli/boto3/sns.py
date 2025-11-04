#!/usr/bin/python
import boto3

sns_client = boto3.client('sns', region_name='us-east-1')

# Create a topic
response = sns_client.create_topic(Name='my-demo-topic')
topic_arn = response['TopicArn']

print(f"Topic created: {topic_arn}")

# Create a subscription
sns_client.subscribe(
    TopicArn=topic_arn,
    Protocol='email',
    Endpoint='ravi.v@ethnus.com'
)
print("Subscription confirmation email sent. Please confirm it!")

# Publish a message
sns_client.publish(
    TopicArn=topic_arn,
    Message='Hello, this is a test SNS message!',
    Subject='Boto3 SNS Test'
)
print("Message published!")

# Delete a topic
sns_client.delete_topic(TopicArn=topic_arn)
print("Topic deleted!")


'''
| Operation                          | Description                                         |
| ---------------------------------- | --------------------------------------------------- |
| `list_topics()`                    | List all your topics.                               |
| `list_subscriptions_by_topic()`    | See all subscribers of a specific topic.            |
| `unsubscribe(SubscriptionArn=...)` | Remove a subscriber.                                |
| `set_topic_attributes()`           | Set policies, delivery retries, display names, etc. |
'''