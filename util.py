import memcache

client = memcache.Client(['localhost:11211'], debug=True)

def cached_call(f, *args, **kwargs):
    key = str(hash(hash(frozenset(kwargs.items())) + hash(args)))
    result = client.get(key)
    if not result:
        result = f(*args, **kwargs)
        client.set(key, result)
    return result
