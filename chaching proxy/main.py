import argparse
import requests
from flask import Flask,request,Response
from cachetools import TTLCache

cache = TTLCache(maxsize=300,ttl=60)

def start_server(port, origin):
    app = Flask(__name__)
    @app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
    def proxy(path):
        cache_key = request.full_path
        if cache_key in cache:
            cached_response = cache[cache_key]
            response = Response(cached_response.data,cached_response.status_code,cached_response.headers)
            response.headers['X-Cache'] = 'HIT'
        else:
            url = f"{origin}/{path}"
            upstream_response = requests.get(url,params=request.args)
            response = Response(upstream_response.content,upstream_response.status_code,upstream_response.headers.items())
            response.headers['X-Cache'] = 'MISS'
            cache[cache_key] = response
        print(response.headers['X-Cache'])
        return response
    app.run(port=port)
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                                    prog="caching-proxy",
                                    description='caching-proxy --port <number> --origin <url>')
    parser.add_argument("--port",required=True)
    parser.add_argument("--origin",required=True)
    parser.add_argument("--clear-cache",action='store_true')
    args = parser.parse_args()
    if args.clear_cache:
        cache.clear()
        print("cache cleared !")
    try:
        print(f'port :{args.port},origin:{args.origin}')    
        start_server(args.port, args.origin)
    except :
        print(f'failed to run on port :{args.port},origin:{args.origin}')