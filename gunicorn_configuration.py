from multiprocessing import cpu_count


worker_class = 'gthread'
workers = cpu_count() * 2 + 1
threads = 2
keepalive = 300
capture_output = True
access_log = error_log = "/var/www/doiui/gunicorn.log"
