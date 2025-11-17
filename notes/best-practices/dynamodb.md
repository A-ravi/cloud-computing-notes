## Best  Practice of DynamoDB

### Design Principles
- Design for the access patterns, not for the data model.
    - What items you read, how you read them, and how often you read them, based on this design your pk and sk.
- Use single table design wherever possible to reduce the number of queries and improve performance.
- Use Sort key for time, status or hierarchy based queries.
- Avoid large items
- Use GSIs and LSIs judiciously to support additional access patterns.
- Avoid LSI's if possible as they share the same throughput as the base table.
- Don't oversize GSI's, they have their own throughput and can increase costs.
- Use DynamoDB AutoScaling to automatically adjust read and write capacity based on traffic patterns.
- Use DAX for read-heavy workloads to improve performance.
- Use Batch Operations for bulk reads and writes to reduce the number of requests and improve performance.
- Avoid Large Scans, use Query operation with appropriate key conditions and filters.
- Perfer On-Demand mode for unpredictable workloads.
- Use TTL
- Use Multiple access patterns like PK+SK, GSI, LSI to optimize data retrieval.
- use `starts_with` operator on sort key for better query performance.
- use Strong consistent reads only when necessary, as they consume more read capacity units and have higher latency.
-  Use IAM Condtitions to restrict access to specific attributes or items in the table.
- Enable Encryption at rest using AWS KMS for better security.
- Use VPC endpoints to securely connect to DynamoDB without exposing it to the public internet.
- Use Atomic counters for incrementing or decrementing numeric attributes.
- Batch your reads
- Monitor the DynamoDB metrics using CloudWatch to identify performance bottlenecks and optimize your table design.

### Operational Guidelines
- Consider changing the Table class to Standard-IA for tables that are infrequently accessed to save costs.
- Enable Backups (on-demand and continuous) to protect against data loss. (all configuration are included)
- Enable Point-in-Time Recovery (PITR) to restore the table to any point in time within the last 35 days.
- Enable CloudWatch Contributor Insights to analyze and visualize log data from DynamoDB Streams.
- Enable Deletion Protection features to protect from accidental deletition.
- Enable Time To Live (Additional Setting Sections) based on the attribute
- DynamoDB streams to capture item level modifications.
- Delete the Unused tables for cost saving.
