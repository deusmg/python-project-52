import json
import os


def load_json(file):
    with open(os.path.abspath(f'task_manager/fixtures/{file}'), 'r') as f:
        return json.loads(f.read())
