# Главный модуль: консольное меню

from services import BookingService
from strategies import StandardPricing, SeasonalPricing, DynamicPricing
from observers import EmailObserver, LogObserver

BASE_PRICE = 5000   # базовая цена рейса


def vvesti_stroku(soobshenie):
    stroka = input(soobshenie).strip()
    while stroka == "":
        print("Ошибка! Значение не может быть пустым.")
        stroka = input(soobshenie).strip()
    return stroka


def pokazat_menu():
    print("===== МЕНЮ =====")
    print("1. Забронировать билет")
    print("2. Показать билеты")
    print("3. Сменить стратегию цены")
    print("0. Выход")


def main():
    service = BookingService(capacity=10)
    # OBSERVER: подписываем двух наблюдателей
    service.subscribe(EmailObserver())
    service.subscribe(LogObserver())

    while True:
        pokazat_menu()
        vybor = input("Выберите пункт: ").strip()

        if vybor == "1":
            print("Класс: эконом / бизнес / первый")
            class_name = vvesti_stroku("Класс билета: ")
            passenger = vvesti_stroku("Пассажир: ")
            try:
                ticket = service.book(class_name, passenger, BASE_PRICE)
            except ValueError as e:
                print("Ошибка:", e)
            else:
                print(f"Готово: {ticket}")

        elif vybor == "2":
            print()
            if len(service.tickets) == 0:
                print("Билетов пока нет.")
            for t in service.tickets:
                print(t)
            print()

        elif vybor == "3":
            print("Стратегия: 1 - стандартная, 2 - сезонная, 3 - динамическая")
            vybor_strategii = input("Ваш выбор: ").strip()
            if vybor_strategii == "1":
                service.set_strategy(StandardPricing())
                print("Установлена стандартная цена.")
            elif vybor_strategii == "2":
                service.set_strategy(SeasonalPricing())
                print("Установлена сезонная цена (+20%).")
            elif vybor_strategii == "3":
                # динамическая цена зависит от числа уже проданных билетов
                service.set_strategy(DynamicPricing(len(service.tickets), service.capacity))
                print("Установлена динамическая цена.")
            else:
                print("Неизвестная стратегия.")

        elif vybor == "0":
            print("Выход из программы. До свидания!")
            break

        else:
            print("Нет такого пункта меню, попробуйте снова.")


if __name__ == "__main__":
    main()
