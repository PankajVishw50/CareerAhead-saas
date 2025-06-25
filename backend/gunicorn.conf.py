import multiprocessing

workers = multiprocessing.cpu_count() * 2 + 1
bind = "0.0.0.0:7575"
# errorlog = "./logs/gunicorn-server.log"
# accesslog = "./logs/gunicorn-application.log"
loglever = "debug"
worker_class = "uvicorn.workers.UvicornWorker"
# worker_class = "util.uvicornworker.RestartableUvicornWorker"
wsgi_app = "careerahead.asgi:application"
capture_output = True
# reload_engine = "inotify"
