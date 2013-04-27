import os

def numCPUs():
    if not hasattr(os, "sysconf"):
        raise RuntimeError("No sysconf detected.")
    return os.sysconf("SC_NPROCESSORS_ONLN")

bind = "127.0.0.1:8118"
workers = numCPUs() * 2 + 1
pidfile = '/tmp/grandvadrouille.pid'
proc_name = 'gunicorn/grandvadrouille'
daemon = False
debug = False
logfile = "/tmp/grandvadrouille.log"
loglevel = "debug"
