

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

Container:
```
docker build -t gym:latest .

docker run -it \
           -p 8080:8080 \
           -v /Users/jamespenson/Documents/python/gym-class-booker/secrets:/secrets \
           -e GOOGLE_APPLICATION_CREDENTIALS=/secrets/gym-booker-72a4fa622a1e.json \
    gym:latest

curl -X POST \
     -H "Content-Type: application/json" \
     -d @secrets/test-class.json \
     localhost:8080/api/book
```