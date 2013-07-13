import memcache
import urlparse
import urllib

client = memcache.Client(['localhost:11211'], debug=True)

def get_with_back(request):
    def _with_back(url):
        url_parts = urlparse.urlparse(url)
        query_str = url_parts.query
        query = urlparse.parse_qs(query_str)
        new_query = {}
        for k, v in query.iteritems():
            new_query[k] = v[0]
        new_query['back_url'] = request.url
        query_str = urllib.urlencode(new_query)

        url_parts = (
                url_parts.scheme,
                url_parts.netloc,
                url_parts.path,
                url_parts.params,
                query_str,
                url_parts.fragment)
        return urlparse.urlunparse(url_parts)
    return _with_back

def cached_call(f, *args, **kwargs):
    key = str(hash(hash(frozenset(kwargs.items())) + hash(args)))
    result = client.get(key)
    if not result:
        result = f(*args, **kwargs)
        client.set(key, result)
    return result
