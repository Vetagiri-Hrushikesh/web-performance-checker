from app.celery_app import celery  # Make sure this matches the exported instance
import subprocess
import json

@celery.task(bind=True)
def run_lighthouse_audit(self, url):
    command = f"lighthouse {url} --output=json --quiet"
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
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
    return parsed_data
