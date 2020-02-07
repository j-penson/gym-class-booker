from google.cloud import secretmanager_v1beta1 as secretmanager
import ast

# Create the Secret Manager client.
client = secretmanager.SecretManagerServiceClient()


def get_creds(secret_id):
    """Read a secret from GCP secret manager"""
    # Build the resource name of the secret version.
    name = client.secret_version_path('607688776346', secret_id, '1')

    # Access the secret version and return dictionary
    response = client.access_secret_version(name)
    payload = response.payload.data.decode('UTF-8')
    return ast.literal_eval(payload)
