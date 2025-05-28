import os
import json

def parse(dir_key: str, file_name: str):
    json_root = os.getenv(dir_key)
    if json_root is None:
        raise ValueError(f'env for {dir_key} is not set')

    if os.path.exists(file_name):
        with open(file_name, 'r') as file:
            return json.load(file)
    else:
        return []

def save(dir_key: str, file_name: str, data: any):
    json_root = os.getenv(dir_key)
    if json_root is None:
        raise ValueError(f'env for {dir_key} is not set')
    if not os.path.exists(file_name):
        with open(file_name, 'x') as file:
            json.dump(data, file, indent=2)
    else:
        with open(file_name, 'w') as file:
            json.dump(data, file, indent=2)
