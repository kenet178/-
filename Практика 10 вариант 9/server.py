# HTTP-сервер REST API для рейсов.
# Эндпоинты:
#   GET    /flights            — список (фильтр ?origin=, сортировка ?sort=price)
#   GET    /flights/available  — доступные рейсы (спец. операция)
#   GET    /flights/{id}       — один рейс
#   POST   /flights            — создать рейс
#   PUT    /flights/{id}       — изменить рейс
#   DELETE /flights/{id}       — удалить рейс

import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

from service import FlightService

HOST = "127.0.0.1"
PORT = 8000

service = FlightService()


class FlightHandler(BaseHTTPRequestHandler):

    # отправить JSON-ответ с кодом состояния
    def _send(self, code, payload):
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    # прочитать тело запроса (JSON)
    def _read_body(self):
        length = int(self.headers.get("Content-Length", 0))
        if length == 0:
            return {}
        raw = self.rfile.read(length)
        return json.loads(raw.decode("utf-8"))

    # разбить путь на части: "/flights/5" -> ["flights", "5"]
    def _parts(self):
        return [p for p in urlparse(self.path).path.split("/") if p]

    def do_GET(self):
        parts = self._parts()
        query = parse_qs(urlparse(self.path).query)

        if parts == ["flights"]:
            origin = query.get("origin", [None])[0]
            sort = query.get("sort", [None])[0]
            return self._send(200, service.list_all(origin, sort))

        if parts == ["flights", "available"]:
            return self._send(200, service.available())

        if len(parts) == 2 and parts[0] == "flights":
            try:
                flight_id = int(parts[1])
            except ValueError:
                return self._send(400, {"error": "Неверный id"})
            flight = service.get(flight_id)
            if flight is None:
                return self._send(404, {"error": "Рейс не найден"})
            return self._send(200, flight)

        self._send(404, {"error": "Не найдено"})

    def do_POST(self):
        if self._parts() == ["flights"]:
            try:
                data = self._read_body()
            except json.JSONDecodeError:
                return self._send(400, {"error": "Некорректный JSON"})
            # валидация обязательных полей
            if not data.get("number") or "seats" not in data:
                return self._send(400, {"error": "Не хватает полей number/seats"})
            flight = service.create(data)
            return self._send(201, flight)   # 201 Created
        self._send(404, {"error": "Не найдено"})

    def do_PUT(self):
        parts = self._parts()
        if len(parts) == 2 and parts[0] == "flights":
            try:
                flight_id = int(parts[1])
                data = self._read_body()
            except (ValueError, json.JSONDecodeError):
                return self._send(400, {"error": "Некорректный запрос"})
            flight = service.update(flight_id, data)
            if flight is None:
                return self._send(404, {"error": "Рейс не найден"})
            return self._send(200, flight)
        self._send(404, {"error": "Не найдено"})

    def do_DELETE(self):
        parts = self._parts()
        if len(parts) == 2 and parts[0] == "flights":
            try:
                flight_id = int(parts[1])
            except ValueError:
                return self._send(400, {"error": "Неверный id"})
            if not service.delete(flight_id):
                return self._send(404, {"error": "Рейс не найден"})
            return self._send(200, {"deleted": flight_id})
        self._send(404, {"error": "Не найдено"})

    # свой формат журнала запросов
    def log_message(self, format, *args):
        print(f"[HTTP] {self.command} {self.path}")


def main():
    server = HTTPServer((HOST, PORT), FlightHandler)
    print(f"REST API запущен на http://{HOST}:{PORT}")
    server.serve_forever()


if __name__ == "__main__":
    main()
