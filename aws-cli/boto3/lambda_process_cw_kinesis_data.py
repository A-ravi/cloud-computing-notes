import json
import base64
import boto3
import os
import gzip

kinesis_client = boto3.client('kinesis')
KINESIS_DATA_STREAM = os.environ['KinesisDataStream']

def lambda_handler(event, context):
  ### Get CloudWatch Logs records and decode them
  for record in event["Records"]:
    # Set partition key
    pk = str("PartitionKey1")
    # Print partition key to logs for verification and troubleshooting
    print("Partition key: " + str(pk))
    # Decode the log files data from CloudWatch Logs
    payload = base64.b64decode(record["kinesis"]["data"])
    # Print the decoded data to logs for verification and troubleshooting
    print("Decoded payload: " + str(payload))
    # CloudWatch Logs data is delivered in a compressed format and must be decompressed
    message = gzip.decompress(payload)
    # Print decompressed data to logs for verification and troubleshooting
    print("Uncompressed message: " + str(message))

  ### Extract JSON data
  # Load data from CloudWatch logs into memory
  event_data = json.loads(message)
  # Print to logs for verification and troubleshooting
  print("eventData JSON string: " + str(event_data))

  # Extract all top-level and nested keys, then recombine into a single string
  index1 = 0
  top_level_keys = ''
  # Loop to extract the top-level keys
  for key, value in event_data.items():
    index1 += 1
    if key != 'logEvents':
      if index1 < (len(event_data.keys())):
        top_level_keys += f'"{key}": "{value}", '
      else:
        top_level_keys += f'"{key}": "{value}"'
    if key == 'logEvents':
      # Loop to extract the nested keys in the logEvents
      for events in value:
        index2 = 0
        logEvents_keys = ''
        for logEvents_key, logEvents_value in events.items():
          index2 += 1
          if index2 < (len(events.keys())):
            logEvents_keys += f'"{logEvents_key}": "{logEvents_value}", '
          else:
            logEvents_keys += f'"{logEvents_key}": "{logEvents_value}"'
        # Print strings derived from each level of keys and values to validate the for loops are working correctly
        print(f'Top level keys: {top_level_keys}\n')
        print(f'Keys in logEvents: {logEvents_keys}\n')
        # Recombine the extracted top-level and nested keys to create a single string of keys and values
        recombined_message = f'{{{top_level_keys}{logEvents_keys}}}'
        # Convert the combined message string to a dict type
        convert_message_to_dict = json.loads(recombined_message)
        # Print the combined message data to logs for verification and troubleshooting
        print(f'Recombined message: {convert_message_to_dict}')
        # Encode the combined message data into a byte format required for the Kinesis data stream
        encoded_message = json.dumps(convert_message_to_dict, indent=2).encode('utf-8')
        # Print the encoded message data to logs for verification and troubleshooting
        print("Encoded message: " + str(encoded_message))
        # Send encoded extracted data to a Kinesis data stream
        response = kinesis_client.put_record(Data=encoded_message, PartitionKey=pk, StreamName=KINESIS_DATA_STREAM)
        # Print the response from Kinesis to logs for verification and troubleshooting
        print(response)
