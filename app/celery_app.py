from celery import Celery

def make_celery():
    celery = Celery(__name__, broker='redis://localhost:6379/0')
    celery.conf.update(result_backend='redis://localhost:6379/0')
    return celery

celery = make_celery()
