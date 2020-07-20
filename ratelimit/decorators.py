from __future__ import absolute_import

from functools import wraps

from ratelimit import ALL, UNSAFE
from ratelimit.exceptions import Ratelimited
from ratelimit.core import is_ratelimited


__all__ = ['ratelimit']


def ratelimit(group=None, key=None, rate=None, method=ALL, block=False, limit_for=0):
    def decorator(fn):
        @wraps(fn)
        def _wrapped(request, *args, **kw):
            old_limited = getattr(request, 'limited', False)
            ratelimited = is_ratelimited(request=request, group=group, fn=fn,
                                         key=key, rate=rate, method=method,
                                         limit_for=limit_for, increment=True)
            request.limited = ratelimited or old_limited
            if ratelimited and block:
                raise Ratelimited()
            return fn(request, *args, **kw)
        return _wrapped
    return decorator


ratelimit.ALL = ALL
ratelimit.UNSAFE = UNSAFE
