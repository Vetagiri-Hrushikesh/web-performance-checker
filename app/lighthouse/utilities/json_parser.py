import json

def parse_json(data):
    try:
        return json.loads(data)
    except ValueError as e:
        return {"error": str(e)}
