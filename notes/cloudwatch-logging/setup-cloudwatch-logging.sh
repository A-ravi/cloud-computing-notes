
#install the binaries for the cloudwatch agent and collectd

sudo yum install -y amazon-cloudwatch-agent collectd

sudo wget https://aws-tc-largeobjects.s3.us-west-2.amazonaws.com/CUR-TF-200-ACCAP6-91948/capstone-6-security/s3/config.json -P /opt/aws/amazon-cloudwatch-agent/bin/

sudo cat /opt/aws/amazon-cloudwatch-agent/bin/config.json

# Start the cloudwatch agent
sudo /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl -a fetch-config -m ec2 -s -c file:/opt/aws/amazon-cloudwatch-agent/bin/config.json

# check the status of the cloudwatch agent
sudo service amazon-cloudwatch-agent status

# Logs of cloudwatch agent
sudo cat /opt/aws/amazon-cloudwatch-agent/logs/amazon-cloudwatch-agent.log

