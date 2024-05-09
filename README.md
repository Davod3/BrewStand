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
git clone https://github.com/Davod3/BrewStand-CloudComputing-14.git --branch phase4
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

All the following commands should be executed on the Google Cloud Console.

Before deploying the application to GKE, a service account must be created in the IAM Service. To do so, execute the following commands once:

```
gcloud iam service-accounts create brewstand-dataset-sa --project=cloud-computing-project-416422
```

```
gcloud storage buckets add-iam-policy-binding gs://brewstand-datset --member "serviceAccount:brewstand-dataset-sa@cloud-computing-project-416422.iam.gserviceaccount.com" --role "roles/storage.objectViewer"
```

```
gcloud iam service-accounts add-iam-policy-binding brewstand-dataset-sa@cloud-computing-project-416422.iam.gserviceaccount.com --role roles/iam.workloadIdentityUser --member "serviceAccount:cloud-computing-project-416422.svc.id.goog[default/brewstand-sa]"
```

gcloud iam service-accounts add-iam-policy-binding \
    --role roles/iam.workloadIdentityUser \
    --member "serviceAccount:cloud-computing-project-416422.svc.id.goog[default/brewstand-sa]" \
    brewstand-dataset-sa@cloud-computing-project-416422.iam.gserviceaccount.com

gcloud secrets add-iam-policy-binding SECRET_NAME \
    --member=serviceAccount:brewstand-dataset-sa@cloud-computing-project-416422.iam.gserviceaccount.com \
    --role=roles/secretmanager.secretAccessor

To create a cluster on the GKE, you can execute the following commands:

```
gcloud beta container --project "cloud-computing-project-416422" clusters create "brewstand-prod" --no-enable-basic-auth --release-channel "regular" --machine-type "e2-medium" --image-type "COS_CONTAINERD" --disk-type "pd-balanced" --disk-size "50" --metadata disable-legacy-endpoints=true --scopes "https://www.googleapis.com/auth/devstorage.read_only","https://www.googleapis.com/auth/logging.write","https://www.googleapis.com/auth/monitoring","https://www.googleapis.com/auth/servicecontrol","https://www.googleapis.com/auth/service.management.readonly","https://www.googleapis.com/auth/trace.append" --num-nodes "8" --logging=SYSTEM,WORKLOAD --monitoring=SYSTEM --enable-ip-alias --network "projects/cloud-computing-project-416422/global/networks/default" --subnetwork "projects/cloud-computing-project-416422/regions/europe-southwest1/subnetworks/default" --no-enable-intra-node-visibility --default-max-pods-per-node "110" --security-posture=standard --workload-vulnerability-scanning=disabled --no-enable-master-authorized-networks --addons HorizontalPodAutoscaling,HttpLoadBalancing,GcePersistentDiskCsiDriver,GcsFuseCsiDriver --enable-autoupgrade --enable-autorepair --max-surge-upgrade 1 --max-unavailable-upgrade 0 --binauthz-evaluation-mode=DISABLED --enable-managed-prometheus --workload-pool "cloud-computing-project-416422.svc.id.goog" --enable-shielded-nodes --node-locations "europe-southwest1-a" --zone=europe-southwest1-a 
```

```
gcloud container clusters get-credentials brewstand-prod --region=europe-southwest1-a
```

```
kubectl config current-context
```

```
kubectl create serviceaccount brewstand-sa
```

```
kubectl annotate serviceaccount brewstand-sa --namespace default iam.gke.io/gcp-service-account=brewstand-dataset-sa@cloud-computing-project-416422.iam.gserviceaccount.com
```

After the cluster is created, you can deploy the services with the following command:

```
./deploy.sh
```


