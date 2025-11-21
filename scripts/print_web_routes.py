import sys
sys.path.insert(0, '.')
from app import web
for r in web.router.routes:
    methods = getattr(r, 'methods', None)
    endpoint = getattr(r, 'endpoint', None)
    name = endpoint.__name__ if endpoint is not None else '<no-endpoint>'
    print(r.path, methods, name)
