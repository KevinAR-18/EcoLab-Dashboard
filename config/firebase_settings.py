import os
import sys
from pathlib import Path


def _get_base_dir():
    """
    Tentukan base directory berdasarkan mode running (EXE vs script)

    Returns:
        Path: Base directory untuk aplikasi
    """
    if getattr(sys, 'frozen', False):
        # Running dari EXE - gunakan folder yang sama dengan EXE
        base_dir = Path(sys.executable).parent
    else:
        # Running dari script - gunakan project root
        base_dir = Path(__file__).resolve().parent.parent

    return base_dir


BASE_DIR = _get_base_dir()
CREDENTIALS_DIR = BASE_DIR / "credentials"
CLIENT_SECRET = CREDENTIALS_DIR / "client_secret.json"
ENV_FILE = BASE_DIR / ".env"

_FIREBASE_DEFAULTS = {
    "apiKey": "",
    "authDomain": "",
    "databaseURL": "",
    "projectId": "",
    "storageBucket": "",
    "messagingSenderId": "",
    "appId": "",
}

_FIREBASE_ENV_MAP = {
    "apiKey": "ECOLAB_FIREBASE_API_KEY",
    "authDomain": "ECOLAB_FIREBASE_AUTH_DOMAIN",
    "databaseURL": "ECOLAB_FIREBASE_DATABASE_URL",
    "projectId": "ECOLAB_FIREBASE_PROJECT_ID",
    "storageBucket": "ECOLAB_FIREBASE_STORAGE_BUCKET",
    "messagingSenderId": "ECOLAB_FIREBASE_MESSAGING_SENDER_ID",
    "appId": "ECOLAB_FIREBASE_APP_ID",
}

_DEFAULT_ADMIN_SERVICE_ACCOUNT = CREDENTIALS_DIR / "firebase_service_account.json"


def _load_dotenv():
    """Load simple KEY=VALUE pairs from a local .env file."""
    if not ENV_FILE.is_file():
        return

    try:
        for raw_line in ENV_FILE.read_text(encoding="utf-8").splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue

            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            if key and key not in os.environ:
                os.environ[key] = value
    except OSError:
        pass


_load_dotenv()


def get_firebase_config():
    """Build the Firebase web config expected by Pyrebase."""
    config = {}

    for key, env_name in _FIREBASE_ENV_MAP.items():
        config[key] = os.getenv(env_name, _FIREBASE_DEFAULTS[key])

    missing_keys = [key for key, value in config.items() if not value]
    if missing_keys:
        missing_envs = ", ".join(_FIREBASE_ENV_MAP[key] for key in missing_keys)
        raise RuntimeError(
            "Firebase config is incomplete. Set these environment variables: "
            f"{missing_envs}"
        )

    return config


def get_firebase_project_id():
    """Return the project id used by Firestore/Admin SDK flows."""
    project_id = os.getenv("ECOLAB_FIREBASE_PROJECT_ID", _FIREBASE_DEFAULTS["projectId"])
    if not project_id:
        raise RuntimeError(
            "Firebase project ID is missing. Set ECOLAB_FIREBASE_PROJECT_ID."
        )
    return project_id


def get_firebase_web_api_key():
    """Return the Firebase Web API key used by auth requests."""
    api_key = os.getenv("ECOLAB_FIREBASE_API_KEY", _FIREBASE_DEFAULTS["apiKey"])
    if not api_key:
        raise RuntimeError(
            "Firebase web API key is missing. Set ECOLAB_FIREBASE_API_KEY."
        )
    return api_key


def get_admin_service_account_path():
    """Resolve the Admin SDK credential path with an optional env override."""
    configured_path = os.getenv("ECOLAB_FIREBASE_SERVICE_ACCOUNT")
    if configured_path:
        return Path(configured_path)

    return _DEFAULT_ADMIN_SERVICE_ACCOUNT


def get_env(name, default=""):
    """Read an environment variable after .env has been loaded."""
    return os.getenv(name, default)


def get_required_env(name):
    """Read a required environment variable and raise if missing."""
    value = os.getenv(name, "").strip()
    if not value:
        raise RuntimeError(f"Required environment variable is missing: {name}")
    return value


def get_env_bool(name, default=False):
    """Read a boolean environment variable."""
    value = os.getenv(name)
    if value is None:
        return bool(default)
    return value.strip().lower() in {"1", "true", "yes", "on"}
