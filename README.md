# start with docker compose

```bash
docker-compose up -d
```

for dev mode (if the source changed)

```bash
docker-compose up -d --build
```

# with minikube

## setup

compile images with docker

```bash
docker build -t api . # in api folder
docker build -t front . # in front folder
```

```bash
minikube start
```

```bash
minikube image load api
minikube image load front
```

## aplly changes

```bash
kubectl apply -f k8s
```

## check changes on dashboard

```bash
minikube dashboard
```

## test it

```bash
kubectl port-forward service/api-service 3000:80 # map port 3000 so we can access the api at localhost:3000
minikube service front-service # open website
```
