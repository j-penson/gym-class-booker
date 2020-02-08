

## Scheduler
Submit a job to log into the website 48 hours before the class

## Booker
1. Log in to website https://URL/login/
2. Go to timetable https://URL/timetable/
3. Get date and navigate
4. Select class
5. Book - see you're all set message

### Tests (run during pipeline)

flake8 style enforcement:

`flake8 --ignore=E203,C901,E402,E501,D400 --max-line-length=160 app/ test/ main.py`

Bandit security linting:

`bandit main.py`

Pytest unit tests:

`python3 -m pytest`

### Build and run locally
Local:
```
export GOOGLE_APPLICATION_CREDENTIALS=./secrets/gym-booker-72a4fa622a1e.json
python main.py
gunicorn -b 0.0.0.0:8080 main:app
```

cd
Container:
```
docker build -t gym:latest .

docker run -it \
           -p 8080:8080 \
           -v /Users/jamespenson/Documents/python/gym-class-booker/secrets:/secrets \
           -e GOOGLE_APPLICATION_CREDENTIALS=/secrets/gym-booker-72a4fa622a1e.json \
    gym:latest
```

### Cloud Build and Run
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

gcurl $(gcloud run services list --platform managed | cut -d" " -f7)"/book"
```

Give Cloud Run access to secrets by adding `Secret Manager Accessor` to the compute service account.


### Cloud Scheduler


```
Create a service account
gcloud iam service-accounts create gym-booker-scheduler \
   --display-name "DISPLAYED-SERVICE-ACCOUNT_NAME

SERVICE_URL=https://gym-booker-5exxbtdepa-ew.a.run.app/book

gcloud beta scheduler jobs create http test-job --schedule "30 17 * * *" \
   --http-method=GET \
   --uri="${SERVICE_URL}" \
   --oidc-service-account-email=gym-scheduler@gym-booker.iam.gserviceaccount.com   \
   --oidc-token-audience="${SERVICE_URL}"

```