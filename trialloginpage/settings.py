import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
CLIENT_SECRET = BASE_DIR / "client_secret.json"

_FIREBASE_DEFAULTS = {
    "apiKey": "AIzaSyDkca9-2rrP1_wetueUq-TbX-HTCrA_sCw",
    "authDomain": "cobaloginpage.firebaseapp.com",
    "databaseURL": "https://cobaloginpage-default-rtdb.asia-southeast1.firebasedatabase.app",
    "projectId": "cobaloginpage",
    "storageBucket": "cobaloginpage.firebasestorage.app",
    "messagingSenderId": "204601095466",
    "appId": "1:204601095466:web:556f5b16bc20eccb679a53",
}

_FIREBASE_ENV_MAP = {
    "apiKey": "TRIALLOGIN_FIREBASE_API_KEY",
    "authDomain": "TRIALLOGIN_FIREBASE_AUTH_DOMAIN",
    "databaseURL": "TRIALLOGIN_FIREBASE_DATABASE_URL",
    "projectId": "TRIALLOGIN_FIREBASE_PROJECT_ID",
    "storageBucket": "TRIALLOGIN_FIREBASE_STORAGE_BUCKET",
    "messagingSenderId": "TRIALLOGIN_FIREBASE_MESSAGING_SENDER_ID",
    "appId": "TRIALLOGIN_FIREBASE_APP_ID",
}


def get_firebase_config():
    config = {}

    for key, env_name in _FIREBASE_ENV_MAP.items():
        config[key] = os.getenv(env_name, _FIREBASE_DEFAULTS[key])

    return config
