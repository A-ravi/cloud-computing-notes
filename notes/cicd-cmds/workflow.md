## A workflow for CI/CD using AWS CodeCommit, CodeBuild, and CodePipeline

```bash
git init
git branch -m dev 
git add .
git commit -m 'two unmodified copies of the application code'
git remote add origin <repository-URL>
git push -u origin dev

## configure user details
git config --global user.name "ravi"
git config --global user.email ravi@example.com
```

### Docker file nodejs application:

```Dockerfile
FROM node:11-alpine
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
COPY . .
RUN npm install
EXPOSE 8080
CMD ["npm", "run", "start"]
```

### Build the docker image
```bash
docker build -t app .
``` 

### tag and push the docker image to ECR
```bash
account_id=$(aws sts get-caller-identity |grep Account|cut -d '"' -f4)

# Verify that the account_id value is assigned to the $account_id variable
echo $account_id

# Tag the app image
docker tag app:latest $account_id.dkr.ecr.us-east-1.amazonaws.com/app:latest

# Push the app image to ECR
docker push $account_id.dkr.ecr.us-east-1.amazonaws.com/app:latest
```
