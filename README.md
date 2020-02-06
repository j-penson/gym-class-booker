

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
```
docker build -t gym:latest .
docker run -it -p 8080:8080 gym:latest
```

### Cloud Run
Deploy commands
```
gcloud builds submit --tag gcr.io/gym-booker/gym

gcloud run deploy gym-booker --image gcr.io/gym-booker/gym \
                             --project gym-booker \
                             --platform managed \
                             --region=europe-west1 \
                             --quiet
```

Github secret: service account with cloud build and run access. Encore json key as base64 `base64 ./secrets/account.json`