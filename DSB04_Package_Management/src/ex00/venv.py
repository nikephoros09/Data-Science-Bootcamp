
import os

venv = os.getenv("VIRTUAL_ENV")
if venv:
    print(f"Your current virtual env is {venv}")
else:
    print("You are not in a virtual environment")
