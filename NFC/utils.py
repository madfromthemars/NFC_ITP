import os
import json
from dotenv import load_dotenv

load_dotenv()

CLIENT_URL: str = os.getenv('CLIENT_URL')
SERVER_URL: str = os.getenv('SERVER_URL')
ACCESS_TOKEN_LIFE_TIME_M: int = int(os.getenv('ACCESS_TOKEN_LIFE_TIME_M'))
REFRESH_TOKEN_LIFE_TIME_H: int = int(os.getenv('REFRESH_TOKEN_LIFE_TIME_H'))

