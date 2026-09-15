from models import Room, StandardRoom, LuxuryRoom
from operations import (
    free_rooms, room_numbers, rooms_by_price, most_expensive_room,
    has_free_room, all_more_expensive, total_price,
)
from generators import rooms_by_category, free_rooms_generator, RoomIterator


# Ввод целого неотрицательного числа
def vvesti_chislo(soobshenie):
    while True:
        try:
            znachenie = int(input(soobshenie).strip())
        except ValueError:
            print("Ошибка! Нужно ввести целое число.")
        else:
            if znachenie < 0:
                print("Ошибка! Число не может быть отрицательным.")
            else:
                return znachenie


def sozdat_nomera():
    return [
        StandardRoom("101", 3000, 2),
        LuxuryRoom("201", 5000, 2),
        StandardRoom("102", 2500, 1, "занят"),
        LuxuryRoom("202", 8000, 3),
        StandardRoom("103", 3500, 2, "занят"),
    ]


def pokazat_menu():
    print("===== МЕНЮ =====")
    print("1. Показать все номера")
    print("2. Свободные номера (filter)")
    print("3. Список номеров комнат (map)")
    print("4. Сортировка по стоимости (sorted)")
    print("5. Статистика (comprehension, any/all, reduce)")
    print("6. Запустить генератор по категории")
    print("7. Свой итератор (по одному через next)")
    print("0. Выход")


def main():
    rooms = sozdat_nomera()   

    while True:
        pokazat_menu()
        vybor = input("Выберите пункт: ").strip()

        if vybor == "1":
            print()
            for room in rooms:
                print(room)     
            print()

        elif vybor == "2":
            svobodnye = free_rooms(rooms)
            print()
            print("Свободные номера:")
            for room in svobodnye:
                print(room)
            print()

        elif vybor == "3":
            numbers = room_numbers(rooms)
            print("Номера комнат:", numbers)

        elif vybor == "4":
            otsortirovano = rooms_by_price(rooms)
            print()
            print("Номера по возрастанию цены:")
            for room in otsortirovano:
                print(room)
            print()

        elif vybor == "5":
            print()
            print("СТАТИСТИКА")
            print("---------")
            print(f"Общая стоимость за ночь: {total_price(rooms)} руб")
            print(f"Есть свободные номера: {has_free_room(rooms)}")     # any
            print(f"Все номера дороже 1000: {all_more_expensive(rooms, 1000)}")  # all
            dorogoy = most_expensive_room(rooms)                        # reduce
            if dorogoy is not None:
                print(f"Самый дорогой номер: {dorogoy}")
            print()

        elif vybor == "6":
            category = input("Категория (Стандарт/Люкс): ").strip()
            print()
            print(f"Номера категории '{category}':")
            nashli = False
            for room in rooms_by_category(rooms, category):
                print(room)
                nashli = True
            if not nashli:
                print("Ничего не найдено.")
            print()

        elif vybor == "7":
            it = RoomIterator(rooms)
            skolko = vvesti_chislo("Сколько номеров показать? ")
            print()
            for i in range(skolko):
                try:
                    room = next(it)     
                except StopIteration:
                    print("Номера закончились.")
                    break
                else:
                    print(room)
            print()

        elif vybor == "0":
            print("Выход из программы. До свидания!")
            break

        else:
            print("Нет такого пункта меню, попробуйте снова.")


if __name__ == "__main__":
    main()
