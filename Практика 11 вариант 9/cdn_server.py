from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.request import urlopen
from urllib.error import URLError
import re
from time import monotonic

CACHE = {}
TTL_SECONDS = 60
ORIGIN = 'http://127.0.0.1:9100'


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if not re.fullmatch(r'/aircraft_[123]\.svg', self.path):
            self.send_error(404, 'Ресурс не найден')
            return
        entry = CACHE.get(self.path)
        fresh = entry is not None and monotonic() - entry[0] < TTL_SECONDS
        try:
            if fresh:
                stored_at, content = entry
            else:
                with urlopen(ORIGIN + self.path, timeout=2) as response:
                    content = response.read()
                stored_at = monotonic()
                CACHE[self.path] = (stored_at, content)
        except URLError:
            self.send_error(502, 'Origin недоступен')
            return
        self.send_response(200)
        self.send_header('Content-Type', 'image/svg+xml')
        self.send_header('Cache-Control', 'public, max-age=60')
        self.send_header('X-Cache', 'HIT' if fresh else 'MISS')
        self.send_header('Age', str(int(monotonic() - stored_at)))
        self.send_header('Content-Length', str(len(content)))
        self.end_headers()
        self.wfile.write(content)

if __name__ == '__main__':
    print('Учебная CDN-модель: http://127.0.0.1:9101/aircraft_1.svg')
    ThreadingHTTPServer(('127.0.0.1', 9101), Handler).serve_forever()
