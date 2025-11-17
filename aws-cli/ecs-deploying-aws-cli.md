# Build and Deploy Containers using Amazon Elastic Container Service (ECS)

```bash
# check the DOckerfile
cat Dockerfile

# build the docker image
docker build -t myapp .

# run and check locally
docker run -p 80:80 myapp

# create a ECR repository
export REPO_URI=$(\
aws ecr create-repository \
 --repository-name myapp \
 --image-tag-mutability IMMUTABLE \
 --query 'repository.repositoryUri'\
 --output text)

# get the aws region
export AWS_REGION=us-east-1

# get the account id
export ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)

# login to ECR
aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com

# tag the image with ECR repo URI
docker tag storyizer/website:latest $REPO_URI:latest

# push the image to ECR
docker push $REPO_URI:latest
```
Task Defination JSON file:
```JSON
{
  "containerDefinitions": [
    {
      "name": "Storyizer-Site",
      "image": "$WEBSITE_URI:latest",
      "essential": true,
      "portMappings": [
        {
          "containerPort": 80,
          "hostPort": 80,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {
          "name": "Port",
          "value": "80"
        },
        {
          "name": "ServerName",
          "value": "Storyizer-site"
        },
        {
          "name": "APIELB",
          "value": "$ALB_DNS_NAME"
        },
        {
          "name": "SaveELB",
          "value": "$ALB_DNS_NAME"
        }
      ],
      "memory": 300,
      "cpu": 512
    }
  ]
}
```
```bash
# replace the environment variables in the task defination file

for json_file in ~/scripts/*.json; do
    tempvalues=$(mktemp)
    envsubst < "$json_file" > "$tempvalues"
    mv "$tempvalues" "$json_file"
done

WEB_TASK_DEF=$(aws ecs register-task-definition --family webSite --cpu 512 --memory 300 --requires-compatibilities EC2 --network-mode bridge --execution-role-arn arn:aws:iam::$ACCOUNT_ID:role/ecsTaskExecutionRole --cli-input-json file://~/file.json --query 'taskDefinition.taskDefinitionArn' --output text)


WEB_TARGET_GROUP_ARN=$(aws elbv2 describe-target-groups --names WebSiteTG80 --query 'TargetGroups[0].TargetGroupArn' --output text)

aws ecs create-service --service-name WebSiteService --cluster arn:aws:ecs:$AWS_REGION:$ACCOUNT_ID:cluster/Storyizer-Cluster --desired-count 2 --load-balancers targetGroupArn=$WEB_TARGET_GROUP_ARN,containerName=Storyizer-Site,containerPort=80 --role arn:aws:iam::$ACCOUNT_ID:role/ECSServiceRole --task-definition "$WEB_TASK_DEF" --launch-type EC2 --query 'service.serviceArn' --output text

# check the ALB DNS name after 5 mins
```