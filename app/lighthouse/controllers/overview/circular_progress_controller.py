import json
import time
from flask import Blueprint, Response, jsonify, request, stream_with_context
from app.redis_client import redis_client
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
        while True:
            latest_result = redis_client.get(task_id)
            print(latest_result)
            if latest_result:
                yield f"data: {latest_result}\n\n"
            else:
                yield "data: {}\n\n".format(json.dumps({"status": "waiting for next update"}))
            time.sleep(5)

    return Response(stream_with_context(stream()), mimetype='text/event-stream')
