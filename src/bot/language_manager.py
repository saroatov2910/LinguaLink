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

# Update user language preference in Firestore (global setting)
def update_user_language(user_id: int, language_code: str):
    """
    Updates or sets the preferred language for a user in Firestore.
    This setting is global for the user across all chats.
    """
    try:
        user_ref = db.collection('users').document(str(user_id))
        user_ref.set({'language': language_code}, merge=True)
        print(f"Language for user {user_id} updated to '{language_code}' in Firestore.")
    except Exception as e:
        print(f"Error updating user language in Firestore: {e}")
