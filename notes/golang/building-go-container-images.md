# Building Go Container Images

## How to running Go application locally
```go
// main.go
package main
import (
  "fmt"
  "net/http"
)
func handler(w http.ResponseWriter, r *http.Request) {
  fmt.Fprintln(w, "Hello from Go")
}
func main() {
  http.HandleFunc("/", handler)
  http.ListenAndServe(":8080", nil)
}
```
To run it first we need to build it and then we run the binary it.
```bash
go build -o myapp main.go
./myapp
```
Then we can access it on `http://localhost:8080`.

## Building a Container Image
To containerize the Go application, we need to create a `Dockerfile`.
```Dockerfile
# Use the official Golang image to build the application
FROM golang:1.20 AS builder
WORKDIR /app

COPY . .
# Force static binary this enable to run on linux p
RUN CGO_ENABLED=0 GOOS=linux go build -o myapp main.go

# Use a minimal image to run the application
FROM alpine:latest
WORKDIR /app
COPY --from=builder /app/myapp .

EXPOSE 8080
CMD ["./myapp"]

```
To build the Docker image, run the following command in the terminal:
```bash
docker build -t app:tag .
```
Once the image is built, you can run the container using:
```bash
docker run -p 8080:8080 app:tag
```
Now you can access the application at `http://localhost:8080`.

Tag the image and push it to a container registry (e.g., Docker Hub, AWS ECR, Google Container Registry):
```bash
docker tag app:tag yourusername/app:tag
docker push yourusername/app:tag
```

### Static linking
By default, Go builds dynamically linked binaries. To create a statically linked binary, you can set the `CGO_ENABLED` environment variable to `0` and specify the target OS using `GOOS`. This is particularly useful when you want to run your Go application in a minimal container image like `alpine`.
```bash
# Linux amd64
CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -o myapp-linux-amd64 main.go

# Linux arm64 (Raspberry Pi, AWS Graviton, M1/M2)
CGO_ENABLED=0 GOOS=linux GOARCH=arm64 go build -o myapp-linux-arm64 main.go

# Windows amd64
GOOS=windows GOARCH=amd64 go build -o myapp.exe main.go

# macOS (Intel)
GOOS=darwin GOARCH=amd64 go build -o myapp-darwin-amd64 main.go
```
 If you delete overlay folder, then just do `# docker system prune -a` this will remove all the unwanted images  and you can start again use docker.