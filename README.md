# BrewStand Application

## Overview
This is the definition of the REST API for the BrewStand application. With this API users will be able to 
create and obtain account tokens, view and compare beer types, as well as order beer in bulk from the
available types

## Requirements
Docker

Docker Compose

## Installation

To install this application simply clone this repository in your desired location. To clone the latest release use the following command, filling in your credentials as required:

```
git clone https://github.com/Davod3/BrewStand-CloudComputing-14.git --branch phase8
```

Afterwards, download the Brewery Operations and Market Analysis Dataset (https://www.kaggle.com/datasets/ankurnapa/brewery-operations-and-market-analysis-dataset) and rename it to dataset.csv.

Once you're done with that, simply create a folder called dataset in the root directory of the cloned repository and move the .csv file there, 
such that its path will be /dataset/datset.csv

Alternatively, you can create the /dataset folder and download the dataset into there from google cloud storage with the following command:

```
wget https://storage.googleapis.com/brewstand-datset/dataset.csv
```

## Usage
To run all the services locally, please execute the following from the root directory:

```
./start.sh
```

Keep in mind that the first time you run the application data might not be immediately available, as the dataset is still being loaded.

During this time, inventory_repository will stop and restart multiple times as it attempts to connect to the postgres db which takes a little longer to start up. This is completely normal.

If all the micro services started successfully, their APIs should be accessible as follows:

Inventory API:
```
http://localhost:3001/ui
```

User API:
```
http://localhost:3002/ui
```

Review API:
```
http://localhost:3003/ui
```

Order API:
```
http://localhost:3004/ui
```

Payment API:
```
http://localhost:3005/ui
```

If the application is being run on a google cloud vm, please replace localhost with the web preview url for the desired port followed by /ui, such as this example for port 3006:

```
https://3006-cs-866602736120-default.cs-europe-west1-iuzs.cloudshell.dev/ui/
```

To stop the execution run the following from the root directory:

```
./stop.sh
```

## Deployment

Brewstand is deployed to a Kubernetes cluster in the GKE Google Cloud service. This deploymnent is managed by a Jenkins pipeline, described in the jenkinsfile located at the root of this repository.
The Jenkins pipeline runs a unit test set and if everything is executed successfully deploys the application to a staging environment, located in a second GKE cluster, for further testing. After running an integration test set with success Jenkins starts the deployment of the changes to the production environment. To shift the application from cluster to cluster Jenkins takes advantage of ArgoCD.

To access the Jenkins Web UI go to: http://34.0.221.12:8080

To access the ArgoCD Web UI go to: http://34.175.18.64:80

All the following commands must be ran in an environment with both Google Cloud Console and Kubectl installed. We recommend Google Cloud Shell.

### Service Accounts

To be able to access all the required resources from Google Cloud, the following commands should be used to create and configure all required service accounts:

```
gcloud iam service-accounts create brewstand-dataset-sa --project=cloud-computing-project-416422
```

```
gcloud storage buckets add-iam-policy-binding gs://brewstand-datset --member "serviceAccount:brewstand-dataset-sa@cloud-computing-project-416422.iam.gserviceaccount.com" --role "roles/storage.objectViewer"
```

```
gcloud iam service-accounts add-iam-policy-binding brewstand-dataset-sa@cloud-computing-project-416422.iam.gserviceaccount.com --role roles/iam.workloadIdentityUser --member "serviceAccount:cloud-computing-project-416422.svc.id.goog[default/brewstand-sa]"
```

### Kubernetes Clusters

As mentioned before, the application uses two clusters for its production and staging environments. We will refer to them as Brewstand-staging and Brewstand-production.
If at any point the clusters must be deleted, then the steps to rebuild them are as follows:

1 - Create the staging cluster with:

```
gcloud beta container --project "cloud-computing-project-416422" clusters create "brewstand-staging" --no-enable-basic-auth --release-channel "regular" --machine-type "e2-standard-4" --image-type "COS_CONTAINERD" --disk-type "pd-balanced" --disk-size "30" --metadata disable-legacy-endpoints=true --scopes "https://www.googleapis.com/auth/devstorage.read_only","https://www.googleapis.com/auth/logging.write","https://www.googleapis.com/auth/monitoring","https://www.googleapis.com/auth/servicecontrol","https://www.googleapis.com/auth/service.management.readonly","https://www.googleapis.com/auth/trace.append" --num-nodes "2" --logging=SYSTEM,WORKLOAD --monitoring=SYSTEM --enable-ip-alias --network "projects/cloud-computing-project-416422/global/networks/default" --subnetwork "projects/cloud-computing-project-416422/regions/europe-southwest1/subnetworks/default" --no-enable-intra-node-visibility --default-max-pods-per-node "110" --security-posture=standard --workload-vulnerability-scanning=disabled --no-enable-master-authorized-networks --addons HorizontalPodAutoscaling,HttpLoadBalancing,GcePersistentDiskCsiDriver,GcsFuseCsiDriver --enable-autoupgrade --enable-autorepair --max-surge-upgrade 1 --max-unavailable-upgrade 0 --binauthz-evaluation-mode=DISABLED --enable-managed-prometheus --workload-pool "cloud-computing-project-416422.svc.id.goog" --enable-shielded-nodes --node-locations "europe-southwest1-a" --zone=europe-southwest1-a
```

2 - Switch context to your newly created cluster:

```
gcloud container clusters get-credentials brewstand-staging --region=europe-southwest1-a
```

3 - Install ArgoCD with the following guide:

https://argo-cd.readthedocs.io/en/stable/getting_started/

4 - Configure the staging cluster with the following commands:

```
kubectl create serviceaccount brewstand-sa
```
```
kubectl annotate serviceaccount brewstand-sa --namespace default iam.gke.io/gcp-service-account=brewstand-dataset-sa@cloud-computing-project-416422.iam.gserviceaccount.com
```
```
kubectl create secret generic postgres-secret \
  --from-literal=POSTGRES_DB=<inventory_db_name> \
  --from-literal=POSTGRES_USER=<inventory_db_username> \
  --from-literal=POSTGRES_PASSWORD=<inventory_db_password>
```
```
kubectl create secret generic order-secret \
  --from-literal=MONGO_DB=<order_db_name> \
  --from-literal=MONGO_USER=<order_db_username> \
  --from-literal=MONGO_PASSWORD=<order_db_password>
```
```
kubectl create secret generic payment-secret \
  --from-literal=MONGO_DB=<payment_db_name> \
  --from-literal=MONGO_USER=<payment_db_username> \
  --from-literal=MONGO_PASSWORD=<payment_db_password>
```
```
kubectl create secret generic user-secret \
  --from-literal=MONGO_DB=<user_db_name> \
  --from-literal=MONGO_USER=<user_db_username> \
  --from-literal=MONGO_PASSWORD=<user_db_password>
```
```
kubectl create secret generic oauth2-proxy-secret \
  --from-literal=OAUTH2_PROXY_COOKIE_SECRET=<coookie_secret> \
  --from-literal=OAUTH2_PROXY_CLIENT_SECRET=<client_secret>
```

5 - Create the production cluster with the following command:

```
gcloud beta container --project "cloud-computing-project-416422" clusters create "brewstand-prod" --no-enable-basic-auth --release-channel "regular" --machine-type "e2-standard-4" --image-type "COS_CONTAINERD" --disk-type "pd-balanced" --disk-size "30" --metadata disable-legacy-endpoints=true --scopes "https://www.googleapis.com/auth/devstorage.read_only","https://www.googleapis.com/auth/logging.write","https://www.googleapis.com/auth/monitoring","https://www.googleapis.com/auth/servicecontrol","https://www.googleapis.com/auth/service.management.readonly","https://www.googleapis.com/auth/trace.append" --num-nodes "3" --logging=SYSTEM,WORKLOAD --monitoring=SYSTEM --enable-ip-alias --network "projects/cloud-computing-project-416422/global/networks/default" --subnetwork "projects/cloud-computing-project-416422/regions/europe-southwest1/subnetworks/default" --no-enable-intra-node-visibility --default-max-pods-per-node "110" --security-posture=standard --workload-vulnerability-scanning=disabled --no-enable-master-authorized-networks --addons HorizontalPodAutoscaling,HttpLoadBalancing,GcePersistentDiskCsiDriver,GcsFuseCsiDriver --enable-autoupgrade --enable-autorepair --max-surge-upgrade 1 --max-unavailable-upgrade 0 --binauthz-evaluation-mode=DISABLED --enable-managed-prometheus --workload-pool "cloud-computing-project-416422.svc.id.goog" --enable-shielded-nodes --node-locations "europe-southwest1-a" --zone=europe-southwest1-a
```

6 - Switch context to the production cluster:

```
gcloud container clusters get-credentials brewstand-prod --region=europe-southwest1-a
```

7 - Configure the production cluster with the following commands:

```
kubectl create serviceaccount brewstand-sa
```
```
kubectl annotate serviceaccount brewstand-sa --namespace default iam.gke.io/gcp-service-account=brewstand-dataset-sa@cloud-computing-project-416422.iam.gserviceaccount.com
```
```
kubectl create secret generic postgres-secret \
  --from-literal=POSTGRES_DB=<inventory_db_name> \
  --from-literal=POSTGRES_USER=<inventory_db_username> \
  --from-literal=POSTGRES_PASSWORD=<inventory_db_password>
```
```
kubectl create secret generic order-secret \
  --from-literal=MONGO_DB=<order_db_name> \
  --from-literal=MONGO_USER=<order_db_username> \
  --from-literal=MONGO_PASSWORD=<order_db_password>
```
```
kubectl create secret generic payment-secret \
  --from-literal=MONGO_DB=<payment_db_name> \
  --from-literal=MONGO_USER=<payment_db_username> \
  --from-literal=MONGO_PASSWORD=<payment_db_password>
```
```
kubectl create secret generic user-secret \
  --from-literal=MONGO_DB=<user_db_name> \
  --from-literal=MONGO_USER=<user_db_username> \
  --from-literal=MONGO_PASSWORD=<user_db_password>
```
```
kubectl create secret generic oauth2-proxy-secret \
  --from-literal=OAUTH2_PROXY_COOKIE_SECRET=<coookie_secret> \
  --from-literal=OAUTH2_PROXY_CLIENT_SECRET=<client_secret>
```

8 - Setup a Jenkins instance to create a pipeline using the provided jenkinsfile. The jenkinsfile may need to be updated to include the correct IP addresses and credentials for the ArgoCD instance
previously installed. Use the following guide as a basis:

https://medium.com/@maheshbiradar8887/jenkins-pipeline-with-argo-cd-and-kubernetes-84e9f943cf13

### Management

Once created, the clusters can be resized with the following commands:

```
./start_clusters.sh
```

```
./stop_clusters.sh
```

### Load Testing

To test how the application reacts to changing loads, Locust can be used. In the repository there is a file called locustfile.py that includes base test cases for load testing. This file can be updated as 
necessary.

To run load tests using locust, simply install it following the official guides (https://docs.locust.io/en/stable/installation.html) and swith to the project's root directory. Afterwards run the following command:

```
locust
```










