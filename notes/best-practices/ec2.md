## EC2 Best Practices
### Security
- Use IAM roles and Identity Federation for accessing AWS resources instead of hardcoding credentials (Like Instance profiles).
- Implement principle of least privilege for Security groups (Also think what could be the least potential access needed).
- Use Latest AMI with security patches.
- Use AWS Inspector to scan for vulnerabilities.
- Use AWS Security Hub to monitor EC2 security compliance against best practices.
- Amazon GuardDuty Runtime Monitoring to identify and respond to potential threats to your instances

### Storage
- Use EBS based root devices
- Use separate EBS volumes for OS and Data.
- Use Instance Store for temporary storage needs.
- Encrypt EBS volumes and snapshots.

### Resource Management
- Use Tag to track and Identity the resources.
- Use Auto Scaling groups to manage EC2 instances.
- Check the limit of EC2 instances per region and request limit increase if needed.
- Use AWS Trusted Advisor to inspect your AWS environment and recommend cost saving options.

### Backup and Recovery
- Regulary backup EBS volumes using snapshots.
- Create an AMI (self baked AMI's) for quick recovery.
- Deploy crictical applications across multiple Availability Zones.
- Use Elastic Load Balancer to distribute traffic across multiple instances.
- Configure Monitoring and respond to alarms/Events.
- 
### Networking
- Set the TTL to 255 for your application for IPv4 and IPv6 addresses.

## Quick Helpful Commands
-  To find the latest AMI ID:
   ```bash
   aws ssm get-parameters-by-path --path /aws/service/ami-amazon-linux-latest --query "Parameters[?contains(Name, 'amzn2-ami-hvm-x86_64-gp2')].Value" --output text
   ```
   The public parameters are available from the following paths:
    - **Linux** – `/aws/service/ami-amazon-linux-latest`
    - **Windows** – `/aws/service/ami-windows-latest`
- Launch instance with public parameter
    ``` --image-id resolve:ssm:/aws/service/ami-amazon-linux-latest/al2023-ami-kernel-default-x86_64 ```
- IMDSv2 enforcement on existing instance
   ```bash
   aws ec2 modify-instance-metadata-options --instance-id i-1234567890abcdef0 --http-tokens required --http-endpoint enabled
   --http-put-response-hop-limit <N>
   ```
- Using IMDSv2 to get details
   ```bash
    TOKEN=`curl -X PUT "http://169.254.169.254/latest/api/token" -H "X-aws-ec2-metadata-token-ttl-seconds: 21600"

    curl -H "X-aws-ec2-metadata-token: $TOKEN" http://169.254.169.254/latest/meta-data/
   ```
