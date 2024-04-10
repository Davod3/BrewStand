# Inventory Repository
docker build --tag europe-southwest1-docker.pkg.dev/cloud-computing-project-416422/brewstand-repo/inventory_repository:latest -f inventory_repository/Dockerfile .
docker push europe-southwest1-docker.pkg.dev/cloud-computing-project-416422/brewstand-repo/inventory_repository:latest

#Inventory Service
docker build --tag europe-southwest1-docker.pkg.dev/cloud-computing-project-416422/brewstand-repo/inventory_service:latest -f inventory_service/Dockerfile .
docker push  europe-southwest1-docker.pkg.dev/cloud-computing-project-416422/brewstand-repo/inventory_service:latest

#Inventory Controller
docker build --tag europe-southwest1-docker.pkg.dev/cloud-computing-project-416422/brewstand-repo/inventory_controller:latest -f inventory_controller/Dockerfile .
docker push europe-southwest1-docker.pkg.dev/cloud-computing-project-416422/brewstand-repo/inventory_controller:latest

#Order Controller
docker build --tag europe-southwest1-docker.pkg.dev/cloud-computing-project-416422/brewstand-repo/order_controller:latest -f order_controller/Dockerfile .
docker push europe-southwest1-docker.pkg.dev/cloud-computing-project-416422/brewstand-repo/order_controller:latest

#Order Service
docker build --tag europe-southwest1-docker.pkg.dev/cloud-computing-project-416422/brewstand-repo/order_service:latest -f order_service/Dockerfile .
docker push europe-southwest1-docker.pkg.dev/cloud-computing-project-416422/brewstand-repo/order_service:latest

#Order Repository
docker build --tag europe-southwest1-docker.pkg.dev/cloud-computing-project-416422/brewstand-repo/order_repository:latest -f order_repository/Dockerfile .
docker push europe-southwest1-docker.pkg.dev/cloud-computing-project-416422/brewstand-repo/order_repository:latest

#Payment Controller
docker build --tag europe-southwest1-docker.pkg.dev/cloud-computing-project-416422/brewstand-repo/payment_controller:latest -f payment_controller/Dockerfile .
docker push europe-southwest1-docker.pkg.dev/cloud-computing-project-416422/brewstand-repo/payment_controller:latest

#Payment Service
docker build --tag europe-southwest1-docker.pkg.dev/cloud-computing-project-416422/brewstand-repo/payment_service:latest -f payment_service/Dockerfile .
docker push europe-southwest1-docker.pkg.dev/cloud-computing-project-416422/brewstand-repo/payment_service:latest

#Payment Repository
docker build --tag europe-southwest1-docker.pkg.dev/cloud-computing-project-416422/brewstand-repo/payment_repository:latest -f payment_repository/Dockerfile .
docker push europe-southwest1-docker.pkg.dev/cloud-computing-project-416422/brewstand-repo/payment_repository:latest

#Review Controller
docker build --tag europe-southwest1-docker.pkg.dev/cloud-computing-project-416422/brewstand-repo/review_controller:latest -f review_controller/Dockerfile .
docker push europe-southwest1-docker.pkg.dev/cloud-computing-project-416422/brewstand-repo/review_controller:latest

#Review Service
docker build --tag europe-southwest1-docker.pkg.dev/cloud-computing-project-416422/brewstand-repo/review_service:latest -f review_service/Dockerfile .
docker push europe-southwest1-docker.pkg.dev/cloud-computing-project-416422/brewstand-repo/review_service:latest

#User Controller
docker build --tag europe-southwest1-docker.pkg.dev/cloud-computing-project-416422/brewstand-repo/user_controller:latest -f user_controller/Dockerfile .
docker push europe-southwest1-docker.pkg.dev/cloud-computing-project-416422/brewstand-repo/user_controller:latest

#User Service
docker build --tag europe-southwest1-docker.pkg.dev/cloud-computing-project-416422/brewstand-repo/user_service:latest -f user_service/Dockerfile .
docker push europe-southwest1-docker.pkg.dev/cloud-computing-project-416422/brewstand-repo/user_service:latest

#User Repository
docker build --tag europe-southwest1-docker.pkg.dev/cloud-computing-project-416422/brewstand-repo/user_repository:latest -f user_repository/Dockerfile .
docker push europe-southwest1-docker.pkg.dev/cloud-computing-project-416422/brewstand-repo/user_repository:latest