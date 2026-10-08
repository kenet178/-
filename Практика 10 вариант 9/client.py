# HTTP-клиент REST API: отправляет запросы серверу и печатает ответы.

import json
import urllib.request
import urllib.error
from urllib.parse import quote

BASE = "http://127.0.0.1:8000"


# Универсальная функция HTTP-запроса
def request(method, path, data=None):
    url = BASE + path
    body = json.dumps(data).encode("utf-8") if data is not None else None
    req = urllib.request.Request(url, data=body, method=method,
                                 headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req) as resp:
            return resp.status, json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        # сервер вернул код ошибки (404, 400 и т.д.)
        return e.code, json.loads(e.read().decode("utf-8"))
    except urllib.error.URLError:
        return None, {"error": "Нет соединения с сервером. Запустите server.py"}


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


def print_flights(flights):
    if not isinstance(flights, list) or len(flights) == 0:
        print("  (пусто)")
        return
    for f in flights:
        print(f"  Рейс {f['id']} {f['number']} | {f['origin']}->{f['destination']} | "
              f"{f['price']} руб | свободно: {f['available']}/{f['seats']}")


def pokazat_menu():
    print("===== МЕНЮ КЛИЕНТА =====")
    print("1. Все рейсы (GET)")
    print("2. Доступные рейсы (GET /flights/available)")
    print("3. Рейсы из города с сортировкой по цене")
    print("4. Один рейс по id (GET)")
    print("5. Добавить рейс (POST)")
    print("6. Изменить цену рейса (PUT)")
    print("7. Удалить рейс (DELETE)")
    print("0. Выход")


def main():
    while True:
        pokazat_menu()
        vybor = input("Выберите пункт: ").strip()

        if vybor == "1":
            code, data = request("GET", "/flights")
            print(f"[{code}] Все рейсы:")
            print_flights(data)

        elif vybor == "2":
            code, data = request("GET", "/flights/available")
            print(f"[{code}] Доступные рейсы:")
            print_flights(data)

        elif vybor == "3":
            origin = vvesti_stroku("Город вылета: ")
            # кодируем русский текст для передачи в URL (percent-encoding)
            code, data = request("GET", f"/flights?origin={quote(origin)}&sort=price")
            print(f"[{code}] Рейсы из '{origin}' по возрастанию цены:")
            print_flights(data)

        elif vybor == "4":
            flight_id = vvesti_chislo("id рейса: ")
            code, data = request("GET", f"/flights/{flight_id}")
            print(f"[{code}]", data)

        elif vybor == "5":
            number = vvesti_stroku("Номер рейса: ")
            origin = vvesti_stroku("Откуда: ")
            destination = vvesti_stroku("Куда: ")
            price = vvesti_chislo("Цена: ")
            seats = vvesti_chislo("Мест: ")
            code, data = request("POST", "/flights",
                                 {"number": number, "origin": origin, "destination": destination,
                                  "price": price, "seats": seats, "available": seats})
            print(f"[{code}] Создан рейс:", data)

        elif vybor == "6":
            flight_id = vvesti_chislo("id рейса: ")
            price = vvesti_chislo("Новая цена: ")
            code, data = request("PUT", f"/flights/{flight_id}", {"price": price})
            print(f"[{code}]", data)

        elif vybor == "7":
            flight_id = vvesti_chislo("id рейса: ")
            code, data = request("DELETE", f"/flights/{flight_id}")
            print(f"[{code}]", data)

        elif vybor == "0":
            print("Выход из клиента.")
            break

        else:
            print("Нет такого пункта меню.")


if __name__ == "__main__":
    main()
