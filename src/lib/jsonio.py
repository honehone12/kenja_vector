import os
import json

def parse_from_env(key: str):
    file_name = os.getenv(key)
    if file_name is None:
        raise ValueError(f'env for {key} is not set')

    if os.path.exists(file_name):
        with open(file_name, 'r') as file:
            return json.load(file)
    else:
        return []
