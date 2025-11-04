import boto3

cloudwatch = boto3.client('cloudwatch', region_name='us-east-1')

# list the available metrics
response = cloudwatch.list_metrics(
    Namespace='AWS/EC2',
    MetricName='CPUUtilization'
)
print("===== Print Meterics =====")
for metric in response['Metrics']:
    print(metric)

instance_id = 'i-09a1515c8dd3488a0'

# Get metrics  statistics
from datetime import datetime, timedelta

end_time = datetime.utcnow()
start_time = end_time - timedelta(hours=1)

response = cloudwatch.get_metric_statistics(
    Namespace='AWS/EC2',
    MetricName='CPUUtilization',
    Dimensions=[
        {'Name': 'InstanceId', 'Value': instance_id}
    ],
    StartTime=start_time,
    EndTime=end_time,
    Period=300,  # 5-minute intervals
    Statistics=['Average', 'Maximum']
)
print()
print("===== Average Metrics Statistics =====")
for datapoint in response['Datapoints']:
    print(datapoint)

# Create an alarm
cloudwatch.put_metric_alarm(
    AlarmName='HighCPUUtilization',
    ComparisonOperator='GreaterThanThreshold',
    EvaluationPeriods=2,
    MetricName='CPUUtilization',
    Namespace='AWS/EC2',
    Period=300,
    Statistic='Average',
    Threshold=80.0,
    ActionsEnabled=True,
    AlarmActions=['arn:aws:sns:us-east-1:123456789012:my-sns-topic'],
    AlarmDescription='Alarm when CPU exceeds 80%',
    Dimensions=[
        {'Name': 'InstanceId', 'Value': 'i-0123456789abcdef0'}
    ],
    Unit='Percent'
)

print("Alarm created successfully!")

######################################
# Logging

logs = boto3.client('logs', region_name='us-east-1')

# Create log group
logs.create_log_group(logGroupName='/boto3/demo')

# Create log stream
logs.create_log_stream(
    logGroupName='/boto3/demo',
    logStreamName='app-logs'
)

# Put log events
import time

timestamp = int(round(time.time() * 1000))

logs.put_log_events(
    logGroupName='/boto3/demo',
    logStreamName='app-logs',
    logEvents=[
        {
            'timestamp': timestamp,
            'message': 'Application started successfully!'
        }
    ]
)

print("Log event added!")

# Get logs event
response = logs.get_log_events(
    logGroupName='/boto3/demo',
    logStreamName='app-logs',
    startFromHead=True
)

for event in response['events']:
    print(event['message'])


'''
| Issue                     | Reason                                   | Fix                            |
| ------------------------- | ---------------------------------------- | ------------------------------ |
| No metrics returned       | Wrong namespace or dimension             | Verify namespace + instance ID |
| Log stream already exists | Duplicate name                           | Use unique logStreamName       |
| Alarm not triggering      | Threshold or evaluation period too short | Adjust alarm settings          |
'''