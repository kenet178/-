# Главный модуль

from models import Room
from services import HotelService
from storage import save_to_json, load_from_json, export_to_csv
from exceptions import RoomAlreadyBookedError

# Имена файлов для сохранения
FILENAME_JSON = "hotel.json"
FILENAME_CSV = "hotel.csv"


# Ввод непустой строки
def vvesti_stroku(soobshenie):
    stroka = input(soobshenie).strip()
    while stroka == "":
        print("Ошибка! Значение не может быть пустым.")
        stroka = input(soobshenie).strip()
    return stroka


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


# Показать меню
def pokazat_menu():
    print("===== МЕНЮ =====")
    print("1. Добавить номер")
    print("2. Показать все номера")
    print("3. Забронировать номер")
    print("4. Освободить номер")
    print("5. Найти свободные номера")
    print("6. Рассчитать стоимость проживания")
    print("7. Сохранить данные в JSON")
    print("8. Загрузить данные из JSON")
    print("9. Экспортировать в CSV")
    print("0. Выход")


def main():
    service = HotelService()   

    while True:
        pokazat_menu()
        vybor = input("Выберите пункт: ").strip()

        if vybor == "1":
            # Добавить номер
            number = vvesti_stroku("Номер комнаты: ")
            if service.find_room(number) is not None:
                print("Такой номер уже существует.")
            else:
                category = vvesti_stroku("Категория: ")
                price = vvesti_chislo("Цена за ночь: ")
                capacity = vvesti_chislo("Количество мест: ")
                room = Room(number, category, price, capacity)
                service.add_room(room)
                print("Номер добавлен.")

        elif vybor == "2":
            # Показать все номера
            if len(service.rooms) == 0:
                print("Номеров пока нет.")
            else:
                print()
                for room in service.rooms:
                    print(room)   
                print()

        elif vybor == "3":
            #  Забронировать номер
            number = vvesti_stroku("Номер для брони: ")
            try:
                room = service.book_room(number)
            except RoomAlreadyBookedError as e:
                print("Ошибка бронирования:", e)
            else:
                if room is None:
                    print("Такого номера нет.")
                else:
                    print(f"Номер {number} забронирован.")

        elif vybor == "4":
            # Освободить номер
            number = vvesti_stroku("Номер для освобождения: ")
            room = service.release_room(number)
            if room is None:
                print("Такого номера нет.")
            else:
                print(f"Номер {number} освобождён.")

        elif vybor == "5":
            # Найти свободные номера
            free = service.find_free_rooms()
            if len(free) == 0:
                print("Свободных номеров нет.")
            else:
                print()
                print("Свободные номера:")
                for room in free:
                    print(room)
                print()

        elif vybor == "6":
            # Рассчитать стоимость проживания
            number = vvesti_stroku("Номер комнаты: ")
            if service.find_room(number) is None:
                print("Такого номера нет.")
            else:
                nights = vvesti_chislo("Сколько ночей? ")
                cost = service.calculate_cost(number, nights)
                print(f"Стоимость проживания: {cost} руб")

        elif vybor == "7":
            # Сохранить в JSON 
            data = service.to_list()
            save_to_json(data, FILENAME_JSON)
            print(f"Данные сохранены в {FILENAME_JSON}")

        elif vybor == "8":
            # Загрузить из JSON
            try:
                data = load_from_json(FILENAME_JSON)
            except FileNotFoundError:
                print("Файл не найден. Сначала сохраните данные.")
            else:
                service.load_from_list(data)
                print("Данные загружены.")
            finally:
                print("Операция загрузки завершена.")

        elif vybor == "9":
            # Экспорт в CSV
            data = service.to_list()
            export_to_csv(data, FILENAME_CSV)
            print(f"Данные экспортированы в {FILENAME_CSV}")

        elif vybor == "0":
            print("Выход из программы. До свидания!")
            break

        else:
            print("Нет такого пункта меню, попробуйте снова.")


if __name__ == "__main__":
    main()
