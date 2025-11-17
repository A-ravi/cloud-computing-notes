## Best Practices for Kinesis Data Streams

#### Stream and Shard Design
- Choose partition key that destribute traffic evenly
- Calcuate Shared based on expected throughput
#### Scaling
- Use enhaned Fan-Out for real time consumers
- Use on-demand streams for unpredictable workloads
#### Data Retention and Storage
- Choose retention 24 hours to 7 days
- Use Kinesis Data Firehose for long term storage

#### Security
- Encrypt Stream at Rest
- Use IAM least privilege
- Enable VPC endpoints

#### Availability
- Run consumers across multiple AZs
- Kinesis stores 3 copies acroos AZs

#### Monitoring
- Monitor the key metrics: IncomingBytes, IncomingRecords... etc.