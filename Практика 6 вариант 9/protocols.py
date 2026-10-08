# Протоколы (структурная типизация)

from typing import Protocol


# Протокол: объект умеет отдавать данные для отчёта.
# Любой класс с методом get_report_data() автоматически ему соответствует.
class Reportable(Protocol):
    def get_report_data(self) -> str:
        ...
