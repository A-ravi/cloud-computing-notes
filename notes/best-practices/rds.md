## Best Practices for RDS

### Operational Guidelines
- Use Multi-AZ deployments for high availability and failover support.
- Use metrics to monitor CPU, Memory, storage, and IOPS utilization. Set up Alarms for critical thresholds.
- Plan for some buffer capacity for storage and IOPS to handle unexpected spikes.
- Enable automatic backups (PITR and Snapshot) to occur during the low IOPS window and set an appropriate retention period.
- If application is caching the DNS of the DB instance, ensure that the cache TTL is set to a low value (e.g., 60 seconds) to handle failovers properly.
- Pick RAM enough that the working set of your database fits into memory to reduce disk I/O.
- Use Enhanced Monitoring for real-time insights into the health of your RDS instances (OS level).
- Configure AWS Secrets Manager to automatically rotate the secrets for Amazon RDS instances.
- AWS Security Hub uses security controls to evaluate resource configurations and security standards to help you comply with various compliance frameworks. 

### Other Tips
- Use different port apart from default for better security.
- Dont't share snapshorts publicly, it will give access to data inside the DB.
- If using Aurora, enable Activity Streams for change data capture.
- Enable Backtrack for Aurora to recover to any point in time within retention period.
- Enable Cluster deletion protection for Aurora clusters/Serverless, RDS Instances to prevent accidental deletion.
- Use latest generation instance types for better performance and cost efficiency.
- Enable AWS RDS Transport Encryption (SSL/TLS) for data in transit.
- Copy tags to Snapshots for better resource management.
- Enable Instance Storage Autoscaling for storage management.
- Enable RDS Snapshot Encryption using AWS KMS for data at rest.
- Enable the logs exports to cloudwatch.
- If required, use IAM Database Authentication to manage database access using IAM roles and policies.
- If required, enable instance level events subscription for RDS instances to get notified on critical events.
- Check the average utitlization of CPU, Memory, Storage, IOPS and scale the instance type accordingly.
- Ensure Encryption is enabled for the RDS instance.
- Ensure that RDS is encrypted with KMS CMK for better control over encryption keys.
- Create a cloudwatch alert for the metric: FreeStorageSpace to monitor the available storage space and avoid unexpected outages.
- Use General Purpose SSD type for storage, it ideal for most workloads.
- Don't put the RDS instance in public subnet.
- Use a different master username other than `admin` or `root` for better security.
- Disable public access to the RDS instance unless absolutely necessary.
- Rotate SSL/TLS certificates before they expire to maintain secure connections.
- Identify the underutilized RDS instances using AWS Trusted Advisor and downsize them to save costs.
- Ensure that DB Security Groups follow the principle of least privilege and don't allow access from 0.0.0.0/0 in order to reduce the risk of unauthorized access.
- Use AWS backup Service for centralized backup management and compliance.
