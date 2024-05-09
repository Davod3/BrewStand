gcloud storage buckets add-iam-policy-binding gs://brewstand-datset --member "serviceAccount:brewstand-dataset-sa@cloud-computing-project-416422.iam.gserviceaccount.com" --role "roles/storage.objectViewer"

gcloud iam service-accounts add-iam-policy-binding brewstand-dataset-sa@cloud-computing-project-416422.iam.gserviceaccount.com --role roles/iam.workloadIdentityUser --member "serviceAccount:cloud-computing-project-416422.svc.id.goog[default/brewstand-sa]"

gcloud iam service-accounts add-iam-policy-binding \
    --role roles/iam.workloadIdentityUser \
    --member "serviceAccount:cloud-computing-project-416422.svc.id.goog[default/brewstand-sa]" \
    brewstand-dataset-sa@cloud-computing-project-416422.iam.gserviceaccount.com

gcloud beta container --project "cloud-computing-project-416422" clusters create "brewstand-prod" --no-enable-basic-auth --release-channel "regular" --machine-type "e2-medium" --image-type "COS_CONTAINERD" --disk-type "pd-balanced" --disk-size "50" --metadata disable-legacy-endpoints=true --scopes "https://www.googleapis.com/auth/devstorage.read_only","https://www.googleapis.com/auth/logging.write","https://www.googleapis.com/auth/monitoring","https://www.googleapis.com/auth/servicecontrol","https://www.googleapis.com/auth/service.management.readonly","https://www.googleapis.com/auth/trace.append" --num-nodes "8" --logging=SYSTEM,WORKLOAD --monitoring=SYSTEM --enable-ip-alias --network "projects/cloud-computing-project-416422/global/networks/default" --subnetwork "projects/cloud-computing-project-416422/regions/europe-southwest1/subnetworks/default" --no-enable-intra-node-visibility --default-max-pods-per-node "110" --security-posture=standard --workload-vulnerability-scanning=disabled --no-enable-master-authorized-networks --addons HorizontalPodAutoscaling,HttpLoadBalancing,GcePersistentDiskCsiDriver,GcsFuseCsiDriver --enable-autoupgrade --enable-autorepair --max-surge-upgrade 1 --max-unavailable-upgrade 0 --binauthz-evaluation-mode=DISABLED --enable-managed-prometheus --workload-pool "cloud-computing-project-416422.svc.id.goog" --enable-shielded-nodes --node-locations "europe-southwest1-a" --zone=europe-southwest1-a 

gcloud container clusters get-credentials brewstand-prod --region=europe-southwest1-a

kubectl config current-context

kubectl create serviceaccount brewstand-sa

kubectl annotate serviceaccount brewstand-sa --namespace default iam.gke.io/gcp-service-account=brewstand-dataset-sa@cloud-computing-project-416422.iam.gserviceaccount.com
