class Configuration:
    DEBUG = True
    CELERY_BROKER_URL = 'redis://localhost:6379/0'  # or your Redis URL
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'  # if you are using Redis for results as well