# Главный модуль: консольное меню

from models import Passenger, Plane, Flight, FlightStatus
from services import AirlineService, register_passenger, print_report, inspect_object
from context import OperationBlock


# Ввод непустой строки
def vvesti_stroku(soobshenie):
    stroka = input(soobshenie).strip()
    while stroka == "":
        print("Ошибка! Значение не может быть пустым.")
        stroka = input(soobshenie).strip()
    return stroka


# Ввод целого неотрицательного числа с обработкой исключения
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


# Начальные данные, чтобы было с чем работать
def sozdat_dannye(service):
    p1 = Plane(1, "Boeing 737", 4)
    p2 = Plane(2, "Airbus A320", 3)
    service.add_flight(Flight(1, "SU100", "Москва", "Сочи", p1, FlightStatus.REGISTRATION))
    service.add_flight(Flight(2, "SU200", "Москва", "Казань", p2, FlightStatus.PLANNED))
    service.add_flight(Flight(3, "SU300", "Санкт-Петербург", "Сочи", p1, FlightStatus.REGISTRATION))


def pokazat_menu():
    print("===== МЕНЮ =====")
    print("1. Показать рейсы")
    print("2. Открыть регистрацию на рейс")
    print("3. Зарегистрировать пассажира")
    print("4. Загрузка рейса")
    print("5. Самые загруженные направления")
    print("6. Отчёт по объектам (Protocol)")
    print("7. Интроспекция объекта")
    print("0. Выход")


def main():
    service = AirlineService()
    sozdat_dannye(service)
    schetchik_passazhirov = 100   # для генерации id пассажиров

    while True:
        pokazat_menu()
        vybor = input("Выберите пункт: ").strip()

        if vybor == "1":
            print()
            for flight in service.flights:
                print(flight.get_report_data())
            print()

        elif vybor == "2":
            number = vvesti_stroku("Номер рейса: ")
            flight = service.set_status(number, FlightStatus.REGISTRATION)
            if flight is None:
                print("Рейс не найден.")
            else:
                print(f"Рейс {number}: открыта регистрация.")

        elif vybor == "3":
            number = vvesti_stroku("Номер рейса: ")
            imya = vvesti_stroku("Имя пассажира: ")
            passport = vvesti_stroku("Паспорт: ")
            schetchik_passazhirov = schetchik_passazhirov + 1
            passenger = Passenger(schetchik_passazhirov, imya, passport)
            try:
                # контекстный менеджер журналирует и замеряет операцию
                with OperationBlock("регистрация пассажира"):
                    flight = service.register(number, passenger)
            except ValueError as e:
                print("Ошибка:", e)
            else:
                if flight is None:
                    print("Рейс не найден.")
                else:
                    print(f"Пассажир {imya} зарегистрирован на {number}.")

        elif vybor == "4":
            number = vvesti_stroku("Номер рейса: ")
            flight = service.find_flight(number)
            if flight is None:
                print("Рейс не найден.")
            else:
                zagruzka = service.load_factor(flight)
                print(f"Загрузка рейса {number}: {round(zagruzka, 1)}% "
                      f"({len(flight.passengers)} из {flight.plane.capacity})")

        elif vybor == "5":
            print()
            print("Самые загруженные направления:")
            for napravlenie, kolichestvo in service.busiest_destinations():
                print(f"  {napravlenie}: {kolichestvo} пассажиров")
            print()

        elif vybor == "6":
            # print_report принимает любой объект с методом get_report_data (Protocol)
            print()
            for flight in service.flights:
                print_report(flight)
                print_report(flight.plane)
            print()

        elif vybor == "7":
            number = vvesti_stroku("Номер рейса для интроспекции: ")
            flight = service.find_flight(number)
            if flight is None:
                print("Рейс не найден.")
            else:
                print()
                inspect_object(flight)
                print()

        elif vybor == "0":
            print("Выход из программы. До свидания!")
            break

        else:
            print("Нет такого пункта меню, попробуйте снова.")


if __name__ == "__main__":
    main()
