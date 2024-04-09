# Inventory Repository
docker build --tag europe-southwest1-docker.pkg.dev/cloud-computing-project-416422/brewstand-repo/inventory_repository:latest -f inventory_repository/Dockerfile .
docker push europe-southwest1-docker.pkg.dev/cloud-computing-project-416422/brewstand-repo/inventory_repository:latest

#Inventory Service
docker build --tag europe-southwest1-docker.pkg.dev/cloud-computing-project-416422/brewstand-repo/inventory_service:latest -f inventory_service/Dockerfile .
docker push  europe-southwest1-docker.pkg.dev/cloud-computing-project-416422/brewstand-repo/inventory_service:latest