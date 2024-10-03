import json
import time
from flask import Blueprint, Response, jsonify, request, stream_with_context
from app.lighthouse.services.overview_service import OverviewService
from app.lighthouse.tasks import run_lighthouse_audit

bp = Blueprint('circular_progress', __name__)
service = OverviewService()

@bp.route('/circular-progress/<string:plan>', methods=['GET'])
def circular_progress(plan):
    metrics = service.get_circular_progress(plan)
    return jsonify(metrics), 200


@bp.route('/circular-progress/premium/<string:task_id>', methods=['GET'])
def get_audit_results(task_id):
    def stream():
        while True:  # Keep the loop running indefinitely
            task = run_lighthouse_audit.AsyncResult(task_id)
            if task.ready():
                result = task.get(timeout=1)
                yield "data: {}\n\n".format(json.dumps(result))
                # Optionally, break if you only want to send the final result once
                break
            else:
                yield "data: {}\n\n".format(json.dumps({"status": "pending"}))
            time.sleep(1)  # Wait a bit before checking again

    return Response(stream_with_context(stream()), mimetype='text/event-stream')