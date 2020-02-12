### GCP Cloud Build and Run
Create a service account with the roles:
- `Cloud Build Service Account`
- `Service Account User`
- `Cloud Run Admin`
- `Storage Viewer`

Create a bucket to deploy the logs to (the default bucket requires project owner access...)

Deploy commands:
```
gcloud builds submit --tag gcr.io/gym-booker/gym --gcs-log-dir=gs://gym-booker-build-logs/logs

gcloud run deploy gym-booker --image gcr.io/gym-booker/gym \
                             --project gym-booker \
                             --platform managed \
                             --region=europe-west1 \
                             --quiet
```

Github secret: service account with cloud build and run access. Encore json key as base64 `base64 ./secrets/account.json`

Call service as a developer
```
gcloud run services list --platform managed

# Add auth for user
gcloud run services add-iam-policy-binding gym-booker \
  --member='user:jpenson24@gmail.com' \
  --role='roles/run.invoker' \
  --platform=managed \
  --region=europe-west1

# Add an alias for curl with auth
gcurl='curl --header "Authorization: Bearer $(gcloud auth print-identity-token)"'

gcurl -X POST \
      -H "Content-Type: application/json" \
      -d @secrets/test-class.json \
      $(gcloud run services list --platform managed | cut -d" " -f7)"/api/book"
```

Give Cloud Run access to secrets by adding `Secret Manager Accessor` to the compute service account.