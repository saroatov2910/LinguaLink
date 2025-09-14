import sys
import os

# Add the project root to the Python path to allow imports from 'src'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import firebase_admin
from firebase_admin import credentials, firestore
from src.config import language_codes

def upload_supported_languages():
    """
    Uploads the list of supported languages from config.py to Firestore.
    This is a one-time setup script.
    """
    try:
        # --- Firebase Initialization ---
        SERVICE_ACCOUNT_KEY_PATH = "data/lingualink-d4685-firebase-adminsdk-fbsvc-0e7dcfe69d.json"
        if not os.path.exists(SERVICE_ACCOUNT_KEY_PATH):
            raise FileNotFoundError(f"Firebase service account key not found at: {SERVICE_ACCOUNT_KEY_PATH}")

        if not firebase_admin._apps:
            cred = credentials.Certificate(SERVICE_ACCOUNT_KEY_PATH)
            firebase_admin.initialize_app(cred)

        db = firestore.client()

        # --- Upload Logic ---
        # We will store the settings in a specific document for app configuration.
        settings_ref = db.collection('settings').document('languages')
        
        # The data to upload is a list of the language codes (e.g., 'en', 'he').
        supported_codes = list(language_codes.keys())
        
        settings_ref.set({
            'supported_codes': supported_codes
        })
        
        print("Successfully uploaded supported languages to Firestore:")
        print(supported_codes)

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    upload_supported_languages()
