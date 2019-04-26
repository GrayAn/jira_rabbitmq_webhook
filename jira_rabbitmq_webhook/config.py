import json
import os


def load_config(cfg_path: str) -> dict:
    path = os.path.expanduser(cfg_path)

    with open(path, 'r') as f:
        raw_data = f.read()

    return json.loads(raw_data)
