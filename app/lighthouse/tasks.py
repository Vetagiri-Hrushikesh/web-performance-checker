# app/lighthouse/tasks.py
import time
from app.celery_app import celery
from app.redis_client import redis_client
import subprocess
import json

@celery.task(bind=True)
def run_lighthouse_audit(self, url):
    task_id = self.request.id
    redis_client.set(task_id, "running")  # Mark the task as running

    command = f"lighthouse {url} --output=json --quiet"
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

    # Check the task state stored in Redis
    while process.poll() is None and redis_client.get(task_id) == "running":
        time.sleep(1)

    if redis_client.get(task_id) != "running":
        process.terminate()
        redis_client.delete(task_id)  # Clean up the Redis entry
        return {"status": "terminated"}

    stdout, stderr = process.communicate()
    if stderr:
        return {"error": stderr.decode("utf-8")}

    result = json.loads(stdout)
    parsed_data = {
        "Performance": result['categories']['performance']['score'] * 100,
        "Accessibility": result['categories']['accessibility']['score'] * 100,
        "Best Practices": result['categories']['best-practices']['score'] * 100,
        "SEO": result['categories']['seo']['score'] * 100
    }
    redis_client.delete(task_id)  # Clean up the Redis entry
    return parsed_data
