# Gunicorn configuration file
import multiprocessing

# Server socket
bind = "0.0.0.0:8080"
backlog = 2048

# Worker processes
workers = 2  # Reduced from default (CPU * 2 + 1) since fetcher is I/O bound
worker_class = "sync"
worker_connections = 1000
timeout = 120  # Increased for long-running fetch operations
keepalive = 5

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

# Process naming
proc_name = "fetcher_regional"

# Server mechanics
daemon = False
pidfile = None
umask = 0
user = None
group = None
tmp_upload_dir = None

# Preload app for faster worker spawning
preload_app = True

# Restart workers after this many requests (prevent memory leaks)
max_requests = 10000
max_requests_jitter = 1000
