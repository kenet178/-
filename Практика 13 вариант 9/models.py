from dataclasses import dataclass,field
from datetime import datetime
@dataclass
class Flight:
    number:str
    origin:str
    destination:str
    aircraft:dict
    passengers:list[dict]=field(default_factory=list)
    seats:int=100
    status:str='scheduled'
    departure:str='2026-12-01T10:00:00'
    def as_document(self):
        if self.seats < 0 or not self.number.strip() or not self.origin.strip() or not self.destination.strip():
            raise ValueError('Укажите номер, маршрут и доступные места')
        if self.origin.casefold() == self.destination.casefold():
            raise ValueError('Аэропорты отправления и назначения должны отличаться')
        if self.status not in {'scheduled', 'delayed', 'boarding', 'departed', 'arrived', 'cancelled'}:
            raise ValueError('Неизвестный статус рейса')
        departure = datetime.fromisoformat(self.departure).isoformat(timespec='seconds')
        return vars(self) | {'departure': departure}
