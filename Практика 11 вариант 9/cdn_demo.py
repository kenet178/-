from time import perf_counter
from urllib.request import urlopen

for number in (1, 1, 2, 2, 3, 3):
    url = f'http://127.0.0.1:9101/aircraft_{number}.svg'
    start = perf_counter()
    with urlopen(url, timeout=3) as response:
        size = len(response.read())
        print(
            url, response.status, size, 'байт', f'{(perf_counter() - start) * 1000:.2f} мс',
            {name: response.headers.get(name) for name in ('Content-Type', 'Cache-Control', 'Age', 'X-Cache')},
        )
