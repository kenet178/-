from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from functools import partial

if __name__ == '__main__':
    handler = partial(SimpleHTTPRequestHandler, directory=str(Path(__file__).parent / 'static'))
    print('Origin: http://127.0.0.1:9100/aircraft_1.svg')
    ThreadingHTTPServer(('127.0.0.1', 9100), handler).serve_forever()
