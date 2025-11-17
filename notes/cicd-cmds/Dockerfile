# For Node.js Application
FROM node:11-alpine
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
COPY . .
RUN npm install
EXPOSE 8080
CMD ["npm", "run", "start"]

# For Python Application
FROM python:3.8-slim
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["python", "app.py"]

# For Go Application
FROM golang:1.16-alpine
WORKDIR /app
COPY . .
RUN go build -o main .
EXPOSE 8080
CMD ["./main"]

# for go binary
FROM alpine:latest
WORKDIR /app
RUN apk --no-cache add ca-certificates curl && chmod +x ./main
COPY ./main .
EXPOSE 8080
CMD ["./main"]

