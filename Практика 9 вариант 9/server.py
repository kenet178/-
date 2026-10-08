# TCP-сервер: принимает команды в формате JSON и возвращает ответы.
# Архитектура: Server -> Service -> Repository.

import socket
import threading
import json
import logging

from service import TicketService

HOST = "127.0.0.1"
PORT = 5000

# Логирование операций сервера (Этап 10)
logging.basicConfig(level=logging.INFO, format="%(asctime)s [SERVER] %(message)s")

service = TicketService()
lock = threading.Lock()   # защита общих данных при работе нескольких клиентов


# Разбор одной команды и формирование ответа
def handle_command(request):
    command = request.get("command")
    data = request.get("data", {})

    with lock:   # только один поток одновременно меняет данные
        if command == "list":
            return {"status": "ok", "data": service.list_all()}

        elif command == "get":
            ticket = service.get(data.get("id"))
            if ticket is None:
                return {"status": "error", "error": "Билет не найден"}
            return {"status": "ok", "data": ticket}

        elif command == "create":
            ticket = service.create(data.get("event"), data.get("seat"), data.get("price"))
            return {"status": "ok", "data": ticket}

        elif command == "buy":
            ticket = service.buy(data.get("id"))
            if ticket is None:
                return {"status": "error", "error": "Билет не найден"}
            if ticket == "sold":
                return {"status": "error", "error": "Билет уже продан"}
            return {"status": "ok", "data": ticket}

        elif command == "available":
            return {"status": "ok", "data": service.available(data.get("event"))}

        elif command == "delete":
            ok = service.delete(data.get("id"))
            if not ok:
                return {"status": "error", "error": "Билет не найден"}
            return {"status": "ok", "data": {}}

        else:
            return {"status": "error", "error": "Неизвестная команда"}


# Обработка одного клиента (выполняется в отдельном потоке)
def handle_client(conn, addr):
    logging.info(f"клиент подключился: {addr}")
    conn.settimeout(120)   # тайм-аут соединения (Этап 9)
    with conn:
        # читаем данные построчно (одна строка = одна JSON-команда)
        reader = conn.makefile("r", encoding="utf-8")
        for line in reader:
            line = line.strip()
            if line == "":
                continue
            # обработка ошибок разбора JSON (Этап 8)
            try:
                request = json.loads(line)
            except json.JSONDecodeError:
                response = {"status": "error", "error": "Некорректный JSON"}
            else:
                logging.info(f"команда от {addr}: {request.get('command')}")
                try:
                    response = handle_command(request)
                except Exception as e:
                    response = {"status": "error", "error": str(e)}
            # отправляем ответ (тоже строкой с переносом)
            conn.sendall((json.dumps(response, ensure_ascii=False) + "\n").encode("utf-8"))
    logging.info(f"клиент отключился: {addr}")


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((HOST, PORT))
        server_socket.listen()
        logging.info(f"сервер запущен на {HOST}:{PORT}")
        # многопользовательский режим: каждый клиент — свой поток (Этап 11)
        while True:
            conn, addr = server_socket.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
            thread.start()


if __name__ == "__main__":
    main()
