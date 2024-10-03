from flask import jsonify

def handle_error(e):
    return jsonify({"error": str(e)}), 500
