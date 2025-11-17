## Best Practices for CloudFront
- Always use cloudfront to secure and accelerate the delivery of our web application or static files
- Compress the objects automatically
- Implement Geo-Restriction whenever necessary
- Enable the Standard logging of cloudfront
- Configure to use viewer protocal to HTTPS or HTTP to HTTPs
- Configure a Deafult Root Object for the distribution
- Enable Orgin Access Control for Distribution have S3 as Origin
- Enable Origin Failover, need to create a origin group then only we can cofigure primary and secondary origin in case of failover
- Enable the Origin Shield
- Enable Real-Time Logging (Kinesis Data Streams)
- 

- Field level encryption protects (sensitive information)
- Traffic between CloudFront Distribution and Origin should be encrypted.
- CloudFront Security Policy: Control the TLS version that Cloudfront uses
- Integreate WAF with CloudFront
