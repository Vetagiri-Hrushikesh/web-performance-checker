import subprocess
import json
import time
from app.celery_app import celery  # Ensure this import points to your configured Celery app
from app.redis_client import redis_client  # Ensure Redis client is properly configured

@celery.task(bind=True)
def run_lighthouse_audit(self, url):
    task_id = self.request.id
    redis_client.set(task_id, "running")  # Initialize task state to "running"

    # Continuously run audit while the task state is set to "running"
    while redis_client.get(task_id) == "running":
        command = f"lighthouse {url} --output=json --quiet --chrome-flags=\"--no-sandbox --disable-cache --disable-application-cache --disable-offline-load-stale-cache --disable-gpu-shader-disk-cache\""

        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()

        if stderr:
            # Store error information back to Redis, and continue looping
            redis_client.set(task_id, json.dumps({"error": stderr.decode("utf-8")}))
            time.sleep(10)  # Brief pause on error to prevent immediate re-run
            continue

        if stdout:
            result = json.loads(stdout)
            # Extract and adjust Lighthouse scores for demonstration purposes
            parsed_data = {
                "Performance": result['categories']['performance']['score'] * 100,
                "Accessibility": result['categories']['accessibility']['score'] * 100,
                "Best Practices": result['categories']['best-practices']['score'] * 100,
                "SEO": result['categories']['seo']['score'] * 100
            }
            # Update the Redis with the latest results
            redis_client.set(task_id, json.dumps(parsed_data))

        # Wait for a configured time interval before running the next audit
        time.sleep(60)  # You can adjust this interval based on your requirements

    # Once the loop exits, clean up Redis
    redis_client.delete(task_id)
