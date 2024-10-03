from flask import Flask, request, jsonify
from celery import Celery
import subprocess
import json


app = Flask(__name__)

# Configure Celery
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

@app.route('/start_audit', methods=['POST'])
def start_audit():
    url = request.json.get('url')
    task = run_lighthouse_audit.delay(url)
    return jsonify({"task_id": task.id}), 202

@app.route('/get_results/<task_id>', methods=['GET'])
def get_results(task_id):
    task = run_lighthouse_audit.AsyncResult(task_id)
    if task.state == 'SUCCESS':
        return jsonify(task.result)
    return jsonify({"status": task.state}), 202


@celery.task(bind=True)
def run_lighthouse_audit(self, url):
    command = f"lighthouse {url} --output=json --quiet"
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    stdout, stderr = process.communicate()

    # Parse JSON data
    result = json.loads(stdout)
    parsed_data = {
        "Performance": result['categories']['performance']['score'] * 100,
        "Accessibility": result['categories']['accessibility']['score'] * 100,
        "Best Practices": result['categories']['best-practices']['score'] * 100,
        "SEO": result['categories']['seo']['score'] * 100
    }
    return parsed_data

if __name__ == '__main__':
    app.run(debug=True)
