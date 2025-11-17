## Best Practices for API Gateway

### Security
- Use IAM roles and policies to control access to your API Gateway resources (creating, reading, updating or deleting APIs).
- Enable WAF (Web Application Firewall) to protect your APIs from common web exploits.
- Configure logging of API requests and responses using CloudWatch Logs or Amazon Data Firehose.
- Implement CloudWATCH Alarms to monitor API Gateway metrics and set up notifications for unusual activity.
- Enable AWS Config (detailed view of configuration of resources in APIs), AWS CloudTrail (provide records of actions taken and more specific details), AWS Security Hub.
- Enable request caching to reduce the number of calls made to your backend and improve the latency of requests.
- Enable CloudFront as well
- Enforce Authentication and Authorization using IAM roles, Cognito User Pools, or Lambda Authorizers.
- Ensure that Active tracing with X-Ray is enabled for API Gateway.
- Enable Resource Policies to restrict access to your API Gateway based on source IP addresses, VPC endpoints, or AWS accounts.
- For private endpoints, use VPC Endpoints to securely connect to your API Gateway without exposing it to the public internet, also specify in the resource policy to allow access only from specific VPC endpoints.
- Enable API cache encryption to protect sensitive data stored in the cache at stage level.
- Ensure Content Encoding is enabled to optimize the payload size and improve performance.
