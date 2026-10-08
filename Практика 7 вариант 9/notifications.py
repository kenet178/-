# Слой уведомлений.
# ISP: маленький интерфейс — только один метод notify().
# LSP: любую реализацию можно подставить вместо другой.

from abc import ABC, abstractmethod


# Абстрактный отправитель уведомлений
class Notifier(ABC):
    @abstractmethod
    def notify(self, message):
        ...


class EmailNotifier(Notifier):
    def notify(self, message):
        print(f"[EMAIL] {message}")


class SmsNotifier(Notifier):
    def notify(self, message):
        print(f"[SMS] {message}")
