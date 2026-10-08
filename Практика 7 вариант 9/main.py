# Главный модуль: сборка зависимостей (composition root) и пользовательский интерфейс.
# Интерфейс отделён от бизнес-логики (SRP).

from models import Flight, TicketStatus
from repository import FlightRepository, TicketRepository
from payments import CardPayment, CashPayment
from notifications import EmailNotifier, SmsNotifier
from services import BookingService


def vvesti_stroku(soobshenie):
    stroka = input(soobshenie).strip()
    while stroka == "":
        print("Ошибка! Значение не может быть пустым.")
        stroka = input(soobshenie).strip()
    return stroka


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


def pokazat_menu():
    print("===== МЕНЮ =====")
    print("1. Показать рейсы")
    print("2. Забронировать билет")
    print("3. Оплатить билет")
    print("4. Вернуть билет")
    print("5. Зарегистрировать пассажира")
    print("6. Показать билеты")
    print("0. Выход")


def main():
    # Сборка зависимостей в одном месте.
    # Здесь легко заменить CardPayment на CashPayment или EmailNotifier на SmsNotifier
    # без изменения сервиса — это принципы OCP и DIP.
    flight_repo = FlightRepository()
    ticket_repo = TicketRepository()
    payment = CardPayment()
    notifier = EmailNotifier()
    service = BookingService(flight_repo, ticket_repo, payment, notifier)

    # Начальные рейсы
    flight_repo.add(Flight("SU100", "Москва", "Сочи", 5000, 3))
    flight_repo.add(Flight("SU200", "Москва", "Казань", 4000, 2))

    while True:
        pokazat_menu()
        vybor = input("Выберите пункт: ").strip()

        if vybor == "1":
            print()
            for f in flight_repo.all():
                print(f"{f.number} | {f.origin}->{f.destination} | {f.price} руб | мест: {f.seats}")
            print()

        elif vybor == "2":
            number = vvesti_stroku("Номер рейса: ")
            passenger = vvesti_stroku("Пассажир: ")
            try:
                ticket = service.book(number, passenger)
            except ValueError as e:
                print("Ошибка:", e)
            else:
                print(f"Забронирован билет №{ticket.id}")

        elif vybor == "3":
            ticket_id = vvesti_chislo("Номер билета: ")
            try:
                service.purchase(ticket_id)
            except ValueError as e:
                print("Ошибка:", e)
            else:
                print("Билет оплачен.")

        elif vybor == "4":
            ticket_id = vvesti_chislo("Номер билета: ")
            try:
                service.refund(ticket_id)
            except ValueError as e:
                print("Ошибка:", e)
            else:
                print("Билет возвращён.")

        elif vybor == "5":
            ticket_id = vvesti_chislo("Номер билета: ")
            try:
                service.register(ticket_id)
            except ValueError as e:
                print("Ошибка:", e)
            else:
                print("Пассажир зарегистрирован.")

        elif vybor == "6":
            print()
            tickets = ticket_repo.all()
            if len(tickets) == 0:
                print("Билетов пока нет.")
            for t in tickets:
                print(f"Билет {t.id} | рейс {t.flight_number} | {t.passenger} | {t.status.value}")
            print()

        elif vybor == "0":
            print("Выход из программы. До свидания!")
            break

        else:
            print("Нет такого пункта меню, попробуйте снова.")


if __name__ == "__main__":
    main()
