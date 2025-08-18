from multiprocessing import cpu_count


worker_class = "gthread"
workers = cpu_count() * 2 + 1
threads = 2
keepalive = 300
capture_output = True
accesslog_format = '%({x-forwarded-for}i)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'
accesslog = "/var/www/doiui/gunicorn_access.log"
errorlog = "/var/www/doiui/gunicorn_error.log"
