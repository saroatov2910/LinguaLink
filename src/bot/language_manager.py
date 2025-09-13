import firebase_admin
from firebase_admin import credentials, firestore
import os

# Initialize Firebase Admin SDK
SERVICE_ACCOUNT_KEY_PATH = "data/lingualink-d4685-firebase-adminsdk-fbsvc-0e7dcfe69d.json"

# Check if the service account key file exists
if not os.path.exists(SERVICE_ACCOUNT_KEY_PATH):
    raise FileNotFoundError(f"Service account key file not found at {SERVICE_ACCOUNT_KEY_PATH}")
# Initialize the Firebase app
cred = credentials.Certificate(SERVICE_ACCOUNT_KEY_PATH)
firebase_admin.initialize_app(cred)
# Get a Firestore client
db = firestore.client()