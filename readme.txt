run Celery with those and redis in 

celery -A alx_backend_security beat -l info
celery -A alx_backend_security worker -l info -P solo