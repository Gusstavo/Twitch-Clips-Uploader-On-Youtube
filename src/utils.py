import json


def get_secrets(file):
    with open(file, "r") as f:
        return json.load(f)


def jprint(text):
    print(json.dumps(text, indent=4))