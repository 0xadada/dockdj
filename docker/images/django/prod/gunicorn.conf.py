import multiprocessing

bind = "0.0.0.0:8080"
workers = multiprocessing.cpu_count() * 2 + 1
accesslog = '/var/log/gunicorn/access.log'
loglevel = 'info'
errorlog = '/var/log/gunicorn/error.log'
