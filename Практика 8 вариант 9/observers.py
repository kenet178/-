# Паттерн OBSERVER: наблюдатели подписываются на события
# и получают уведомления, когда что-то происходит.

from abc import ABC, abstractmethod


# Абстрактный наблюдатель
class Observer(ABC):
    @abstractmethod
    def update(self, event):
        ...


# Наблюдатель: отправка e-mail
class EmailObserver(Observer):
    def update(self, event):
        print(f"[EMAIL] {event}")


# Наблюдатель: запись в журнал
class LogObserver(Observer):
    def update(self, event):
        print(f"[LOG] {event}")


# Субъект (издатель): хранит подписчиков и рассылает им события
class BookingSubject:
    def __init__(self):
        self._observers = []

    def subscribe(self, observer):
        self._observers.append(observer)

    def notify(self, event):
        for observer in self._observers:
            observer.update(event)
