import multiprocessing

bind = "127.0.0.1:8000"
workers = multiprocessing.cpu_count() * 2 + 1
proc_name = "atom"
# errorlog = '~/logs/gunicorn.error.log'
# accesslog = '~/logs/gunicorn.access.log'
