from datetime import datetime
from dotenv import load_dotenv
from os import getenv

load_dotenv()
LOG_PATH = getenv('LOG_PATH')

def log(message: str):
    print(message)
    if not LOG_PATH: return
    with open(LOG_PATH, "a") as f:
        f.write(f"{datetime.now()} | {message}\n")