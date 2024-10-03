from flask import Blueprint, jsonify, request
from app.lighthouse.services.overview_service import OverviewService
from app.lighthouse.tasks import run_lighthouse_audit  # Import the Celery task

bp = Blueprint('circular_progress', __name__)
service = OverviewService()

@bp.route('/circular-progress/<string:plan>', methods=['GET'])
def circular_progress(plan):
    metrics = service.get_circular_progress(plan)
    return jsonify(metrics), 200

@bp.route('/start_audit', methods=['POST'])
def start_audit():
    url = request.json.get('url')
    task = run_lighthouse_audit.delay(url)
    return jsonify({"task_id": task.id}), 202

@bp.route('/premium/<string:task_id>', methods=['GET'])
def get_audit_results(task_id):
    task = run_lighthouse_audit.AsyncResult(task_id)
    if task.state == 'SUCCESS':
        return jsonify(task.result)
    return jsonify({"status": task.state}), 202
