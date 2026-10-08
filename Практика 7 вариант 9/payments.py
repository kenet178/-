# Слой оплаты.
# OCP: новый способ оплаты добавляется новым классом, без изменения сервиса.
# SRP: класс отвечает только за оплату/возврат.

from abc import ABC, abstractmethod


# Абстрактный обработчик оплаты (интерфейс)
class PaymentProcessor(ABC):
    @abstractmethod
    def pay(self, amount):
        ...

    @abstractmethod
    def refund(self, amount):
        ...


# Оплата картой
class CardPayment(PaymentProcessor):
    def pay(self, amount):
        print(f"[ОПЛАТА картой] списано {amount} руб")
        return True

    def refund(self, amount):
        print(f"[ВОЗВРАТ на карту] возвращено {amount} руб")
        return True


# Оплата наличными
class CashPayment(PaymentProcessor):
    def pay(self, amount):
        print(f"[ОПЛАТА наличными] принято {amount} руб")
        return True

    def refund(self, amount):
        print(f"[ВОЗВРАТ наличными] выдано {amount} руб")
        return True
