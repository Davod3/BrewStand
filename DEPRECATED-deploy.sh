kubectl apply -f kubernetes/app-secrets.yaml

# Inventory Repository
docker build --tag europe-southwest1-docker.pkg.dev/cloud-computing-project-416422/brewstand-repo/inventory_repository:latest -f inventory_repository/Dockerfile .
docker push europe-southwest1-docker.pkg.dev/cloud-computing-project-416422/brewstand-repo/inventory_repository:latest

#Inventory Service
docker build --tag europe-southwest1-docker.pkg.dev/cloud-computing-project-416422/brewstand-repo/inventory_service:latest -f inventory_service/Dockerfile .
docker push  europe-southwest1-docker.pkg.dev/cloud-computing-project-416422/brewstand-repo/inventory_service:latest

#Inventory Controller
docker build --tag europe-southwest1-docker.pkg.dev/cloud-computing-project-416422/brewstand-repo/inventory_controller:latest -f inventory_controller/Dockerfile .
docker push europe-southwest1-docker.pkg.dev/cloud-computing-project-416422/brewstand-repo/inventory_controller:latest

#Configuration
kubectl apply -f kubernetes/inventory_deployment.yaml

#Order Controller
docker build --tag europe-southwest1-docker.pkg.dev/cloud-computing-project-416422/brewstand-repo/order_controller:latest -f order_controller/Dockerfile .
docker push europe-southwest1-docker.pkg.dev/cloud-computing-project-416422/brewstand-repo/order_controller:latest

#Order Service
docker build --tag europe-southwest1-docker.pkg.dev/cloud-computing-project-416422/brewstand-repo/order_service:latest -f order_service/Dockerfile .
docker push europe-southwest1-docker.pkg.dev/cloud-computing-project-416422/brewstand-repo/order_service:latest

#Order Repository
docker build --tag europe-southwest1-docker.pkg.dev/cloud-computing-project-416422/brewstand-repo/order_repository:latest -f order_repository/Dockerfile .
docker push europe-southwest1-docker.pkg.dev/cloud-computing-project-416422/brewstand-repo/order_repository:latest

#Configuration
kubectl apply -f kubernetes/order_deployment.yaml

#Payment Controller
docker build --tag europe-southwest1-docker.pkg.dev/cloud-computing-project-416422/brewstand-repo/payment_controller:latest -f payment_controller/Dockerfile .
docker push europe-southwest1-docker.pkg.dev/cloud-computing-project-416422/brewstand-repo/payment_controller:latest

#Payment Service
docker build --tag europe-southwest1-docker.pkg.dev/cloud-computing-project-416422/brewstand-repo/payment_service:latest -f payment_service/Dockerfile .
docker push europe-southwest1-docker.pkg.dev/cloud-computing-project-416422/brewstand-repo/payment_service:latest

#Payment Repository
docker build --tag europe-southwest1-docker.pkg.dev/cloud-computing-project-416422/brewstand-repo/payment_repository:latest -f payment_repository/Dockerfile .
docker push europe-southwest1-docker.pkg.dev/cloud-computing-project-416422/brewstand-repo/payment_repository:latest

#Configuration
kubectl apply -f kubernetes/payment_deployment.yaml

#Review Controller
docker build --tag europe-southwest1-docker.pkg.dev/cloud-computing-project-416422/brewstand-repo/review_controller:latest -f review_controller/Dockerfile .
docker push europe-southwest1-docker.pkg.dev/cloud-computing-project-416422/brewstand-repo/review_controller:latest

#Review Service
docker build --tag europe-southwest1-docker.pkg.dev/cloud-computing-project-416422/brewstand-repo/review_service:latest -f review_service/Dockerfile .
docker push europe-southwest1-docker.pkg.dev/cloud-computing-project-416422/brewstand-repo/review_service:latest

#Configuration
kubectl apply -f kubernetes/review_deployment.yaml

#User Controller
docker build --tag europe-southwest1-docker.pkg.dev/cloud-computing-project-416422/brewstand-repo/user_controller:latest -f user_controller/Dockerfile .
docker push europe-southwest1-docker.pkg.dev/cloud-computing-project-416422/brewstand-repo/user_controller:latest

#User Service
docker build --tag europe-southwest1-docker.pkg.dev/cloud-computing-project-416422/brewstand-repo/user_service:latest -f user_service/Dockerfile .
docker push europe-southwest1-docker.pkg.dev/cloud-computing-project-416422/brewstand-repo/user_service:latest

#User Repository
docker build --tag europe-southwest1-docker.pkg.dev/cloud-computing-project-416422/brewstand-repo/user_repository:latest -f user_repository/Dockerfile .
docker push europe-southwest1-docker.pkg.dev/cloud-computing-project-416422/brewstand-repo/user_repository:latest

#Configuration
kubectl apply -f kubernetes/user_deployment.yaml

#NGINX ingress controller
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.10.0/deploy/static/provider/cloud/deploy.yaml

#Ingress
kubectl apply -f kubernetes/ingress.yaml

#Prometheus CM
kubectl create configmap prometheus-cm --from-file kubernetes/prometheus-cm.yaml

#Prometheus
kubectl apply -f kubernetes/prometheus.yaml