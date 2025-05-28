import os
import json

def parse(key: str):
    file_name = os.getenv(key)
    if file_name is None:
        raise ValueError(f'env for {key} is not set')

    if os.path.exists(file_name):
        with open(file_name, 'r') as file:
            return json.load(file)
    else:
        return []

def save(key: str, data: any):
    file_name = os.getenv(key)
    if file_name is None:
        raise ValueError(f'env for {key} is not set')
    if not os.path.exists(file_name):
        with open(file_name, 'x') as file:
            json.dump(data, file, indent=2)
    else:
        with open(file_name, 'w') as file:
            json.dump(data, file, indent=2)
