
Build and run locally
```
docker build -t gym:latest .
docker run -it -p 8080:8080 gym:latest
```


Cloud Run
```
gcloud builds submit --tag gcr.io/gym-booker/gym



gcloud run deploy gym-booker --quiet --image gcr.io/kanyai/gym --project gym-booker --region europe-west2 --platform managed
gcloud run deploy gym-booker --image gcr.io/kanyai/gym --project gym-booker --platform managed



```