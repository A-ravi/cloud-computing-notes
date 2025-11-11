# Istio usage

### Enable sidecar injection in a namespace
```bash
kubectl create namespace app
kubectl label namespace app istio-injection=enabled
```

### Deploy a sample application
```bash
# app.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: hello-v1
  namespace: app
  labels:
    app: hello
    version: v1
spec:
  replicas: 1
  selector:
    matchLabels:
      app: hello
      version: v1
  template:
    metadata:
      labels:
        app: hello
        version: v1
    spec:
      containers:
      - name: hello
        image: hashicorp/http-echo
        args: ["-text=Hello from v1"]

---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: hello-v2
  namespace: app
  labels:
    app: hello
    version: v2
spec:
  replicas: 1
  selector:
    matchLabels:
      app: hello
      version: v2
  template:
    metadata:
      labels:
        app: hello
        version: v2
    spec:
      containers:
      - name: hello
        image: hashicorp/http-echo
        args: ["-text=Hello from v2"]

---
apiVersion: v1
kind: Service
metadata:
  name: hello
  namespace: app
  labels:
    app: hello
spec:
  selector:
    app: hello
  ports:
  - port: 80
    targetPort: 5678
    protocol: TCP
```

### Destionation Rule
```bash
# destinationrule.yaml
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: hello
  namespace: app
spec:
  host: hello
  subsets:
  - name: v1
    labels:
      version: v1
  - name: v2
    labels:
      version: v2
```

### Ingress Gateway and Virtual Service
```bash 
# gateway.yaml
apiVersion: networking.istio.io/v1beta1
kind: Gateway
metadata:
  name: hello-gateway
  namespace: app
spec:
  selector:
    istio: ingressgateway
  servers:
  - port:
      number: 80
      protocol: HTTP
      name: http
    hosts:
    - "*"

---
apiVersion: networking.istio.io/v1
kind: VirtualService
metadata:
  name: hello
  namespace: app
spec:
  gateways:
  - hello-gateway
  hosts:
  - '*'
  http:
  - route:
    - destination:
        host: hello
        subset: v1
      weight: 50
    - destination:
        host: hello
        subset: v2
      weight: 50

```
### get ingress url
```bash
export INGRESS=$(kubectl -n istio-system get svc istio-ingressgateway \
  -o jsonpath='{.status.loadBalancer.ingress[0].hostname}')
echo "http://$INGRESS/"
```


## Some more examples
### Traffic shifting
```bash
apiVersion: networking.istio.io/v1
kind: VirtualService
metadata:
  name: hello
  namespace: app
spec:
  gateways:
  - hello-gateway
  hosts:
  - '*'
  http:
  - route:
    - destination:
        host: hello
        subset: v1
      weight: 90
    - destination:
        host: hello
        subset: v2
      weight: 10
```

### Header Based Routing
```bash
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: hello
  namespace: app
spec:
  hosts:
  - "*"
  gateways:
  - hello-gateway
  http:
  - match:
    - headers:
        user-role:
          exact: admin
    route:
    - destination:
        host: hello.app.svc.cluster.local
        subset: v2
  - route:
    - destination:
        host: hello.app.svc.cluster.local
        subset: v1
```

### Path Based Routing
```bash
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: hello
  namespace: app
spec:
  hosts:
  - "*"
  gateways:
  - hello-gateway
  http:
  - match:
    - uri:
        prefix: "/new"
    route:
    - destination:
        host: hello.app.svc.cluster.local
        subset: v2
  - route:
    - destination:
        host: hello.app.svc.cluster.local
        subset: v1
```
