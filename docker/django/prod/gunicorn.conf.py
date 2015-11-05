import multiprocessing

bind = "0.0.0.0:8080"
workers = multiprocessing.cpu_count() * 2 + 1
loglevel = 'info'
# Log to stdout
accesslog = '-'
# Log to stderr
errorlog = '-'
