## Best Practices for VPC

### Security
- Create separate VPCs for different environments (e.g., development, testing, production).
- Create subnets in multiple AZs for high availability.
- Create public and private subnets pair per AZ.
    - Public Subnets → ALB / NAT 
    Gateways / Bastion
    - Private App Subnets → EC2 / EKS Nodes / ECS Tasks
    - Private Data Subnets → RDS / ElastiCache
- Use Security Groups (instance level) and Network ACLs(subnet level) to control inbound and outbound traffic.
- Use IAM roles and IAM user to manage the access to AWS resources.
- Enable VPC Flow Logs to capture information about the IP traffic going to and from network interfaces in your VPC.
- Use Network Analyzer to identify unintended network access.
- Use AWS Firewall Manager to centrally configure and manage firewall rules across your VPCs.
- Use Amazon GuardDuty for threat detection and continuous monitoring of malicious activity and unauthorized behavior.

### Other Tips
- Use NAT Gateway in each AX for private subnets outbound access.
- Use VPC Endpoints (Gateway and Interface) to privately connect your VPC to supported AWS services.
- Use Security Groups to control East-West Traffic between different tiers of your application.
- Use Security Groupps reference instead of CIDR blocks.
- Enable DNS hostnames and DNS resolution in your VPC.
- Use Different CIDR blocks for different VPCs to avoid IP conflicts.
- VPC Peering Connections Route Tables should not have whole CIDR of the peer VPC, It should have specific subnets only or EC2 instances IP's.
- Restrict inbound/outbound traffic on all ports from NACLs.
- Remove unused VPC Internet Gateways, NAT Gateways, VPC Peering Connections, Virtual Private Gateways and Endpoints to reduce attack surface.
- Control acccess to VPC endpoints using endpoint policies.
- Use VPC endpoints instead of Internet Gateway for accessing AWS services from private subnets.
- Follow a vpc naming convention for easy identification. `vpc-RegionCode-EnvironmentCode-ApplicationStackCode`
