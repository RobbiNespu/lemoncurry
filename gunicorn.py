import multiprocessing

preload_app = True
proc_name = 'lemoncurry'
worker_class = 'gevent'
workers = multiprocessing.cpu_count() * 2 + 1
