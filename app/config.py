import os
import logging

# BE CAREFULLY, You need to change, secret_KEY
SECRET_KEY = os.getenv("SECRET_KEY", "shhhh! it's a secret")


try:
    from private_config import *
except ImportError:
    pass

# infrastructure

DATABASE_REMOTE_URL = os.getenv("DATABASE_REMOTE_URL", remote_db)
WEATHERBIT_API_KEY = os.getenv("WEATHERBIT_API_KEY", apikey)

