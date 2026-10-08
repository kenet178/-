# TCP-клиент: отправляет команды серверу и печатает ответы.

import socket
import json

HOST = "127.0.0.1"
PORT = 5000


# Отправить запрос и получить ответ
def send_request(sock, reader, request):
    sock.sendall((json.dumps(request, ensure_ascii=False) + "\n").encode("utf-8"))
    line = reader.readline()
    return json.loads(line)


def vvesti_stroku(soobshenie):
    stroka = input(soobshenie).strip()
    while stroka == "":
        print("Ошибка! Значение не может быть пустым.")
        stroka = input(soobshenie).strip()
    return stroka


def vvesti_chislo(soobshenie):
    while True:
        try:
            return int(input(soobshenie).strip())
        except ValueError:
            print("Ошибка! Нужно ввести целое число.")


# Красиво напечатать список билетов из ответа
def print_tickets(data):
    if len(data) == 0:
        print("  (пусто)")
        return
    for t in data:
        print(f"  Билет {t['id']} | {t['event']} | место {t['seat']} | "
              f"{t['price']} руб | {t['status']}")


def pokazat_menu():
    print("===== МЕНЮ КЛИЕНТА =====")
    print("1. Список всех билетов")
    print("2. Доступные места")
    print("3. Купить билет")
    print("4. Добавить билет")
    print("5. Получить билет по id")
    print("6. Удалить билет")
    print("0. Выход")


def main():
    # обработка ошибки подключения (сервер не запущен)
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((HOST, PORT))
    except ConnectionRefusedError:
        print("Не удалось подключиться к серверу. Запустите server.py.")
        return

    reader = sock.makefile("r", encoding="utf-8")
    try:
        while True:
            pokazat_menu()
            vybor = input("Выберите пункт: ").strip()

            if vybor == "1":
                answer = send_request(sock, reader, {"command": "list", "data": {}})
                print("Все билеты:")
                print_tickets(answer["data"])

            elif vybor == "2":
                event = input("Мероприятие (Enter — все): ").strip()
                data = {} if event == "" else {"event": event}
                answer = send_request(sock, reader, {"command": "available", "data": data})
                print("Доступные места:")
                print_tickets(answer["data"])

            elif vybor == "3":
                ticket_id = vvesti_chislo("Номер билета: ")
                answer = send_request(sock, reader, {"command": "buy", "data": {"id": ticket_id}})
                if answer["status"] == "ok":
                    print("Билет куплен:", answer["data"])
                else:
                    print("Ошибка:", answer["error"])

            elif vybor == "4":
                event = vvesti_stroku("Мероприятие: ")
                seat = vvesti_stroku("Место: ")
                price = vvesti_chislo("Цена: ")
                answer = send_request(sock, reader,
                                      {"command": "create",
                                       "data": {"event": event, "seat": seat, "price": price}})
                print("Добавлен билет:", answer["data"])

            elif vybor == "5":
                ticket_id = vvesti_chislo("Номер билета: ")
                answer = send_request(sock, reader, {"command": "get", "data": {"id": ticket_id}})
                if answer["status"] == "ok":
                    print("Билет:", answer["data"])
                else:
                    print("Ошибка:", answer["error"])

            elif vybor == "6":
                ticket_id = vvesti_chislo("Номер билета: ")
                answer = send_request(sock, reader, {"command": "delete", "data": {"id": ticket_id}})
                if answer["status"] == "ok":
                    print("Билет удалён.")
                else:
                    print("Ошибка:", answer["error"])

            elif vybor == "0":
                print("Выход из клиента.")
                break

            else:
                print("Нет такого пункта меню.")
    finally:
        sock.close()


if __name__ == "__main__":
    main()
