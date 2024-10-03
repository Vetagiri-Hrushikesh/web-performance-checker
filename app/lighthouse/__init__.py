# lighthouse/__init__.py
from flask import Blueprint, jsonify, request, abort
from app.redis_client import redis_client

lighthouse_bp = Blueprint('lighthouse', __name__)
from .controllers.overview.circular_progress_controller import bp as overview_bp
lighthouse_bp.register_blueprint(overview_bp, url_prefix='/overview')

@lighthouse_bp.route('/start_audit', methods=['POST'])
def start_audit():
    from app.lighthouse.tasks import run_lighthouse_audit
    try:
        url = request.json.get('url')
        if not url:
            abort(400, description="URL is required in the JSON payload.")
        task = run_lighthouse_audit.delay(url)
        return jsonify({"task_id": task.id}), 202
    except Exception as e:
        abort(500, description=str(e))

@lighthouse_bp.route('/stop_audit/<task_id>', methods=['POST'])
def stop_audit(task_id):
    if redis_client.exists(task_id):
        redis_client.set(task_id, "stopped")  # Update the task state to stopped
        return jsonify({"status": "stopping", "task_id": task_id}), 200
    else:
        return jsonify({"error": "Task not found or already stopped"}), 404