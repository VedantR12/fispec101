import os
import firebase_admin
from firebase_admin import credentials


def initialize_firebase():
    if not firebase_admin._apps:
        service_account_path = os.getenv("FIREBASE_SERVICE_ACCOUNT_PATH")

        if not service_account_path:
            raise RuntimeError(
                "FIREBASE_SERVICE_ACCOUNT_PATH environment variable not set"
            )

        cred = credentials.Certificate(service_account_path)
        firebase_admin.initialize_app(cred)
