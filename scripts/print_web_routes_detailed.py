import sys, inspect
sys.path.insert(0, '.')
from app import web
for r in web.router.routes:
    endpoint = getattr(r, 'endpoint', None)
    if endpoint is None:
        print(r.path, 'NO ENDPOINT')
    else:
        try:
            src = inspect.getsourcefile(endpoint)
        except Exception:
            src = '<unknown>'
        lineno = getattr(endpoint, '__code__', None)
        lineno = lineno.co_firstlineno if lineno else '<no-lineno>'
        print(r.path, getattr(r,'methods',None), endpoint.__name__, 'file=', src, 'lineno=', lineno)
