# Модуль с бизнес-логикой гостиницы

from models import Room
from exceptions import RoomAlreadyBookedError


class HotelService:

    def __init__(self):
        self.rooms = []   

    # Добавить номер в гостиницу
    def add_room(self, room):
        self.rooms.append(room)

    # Найти номер по его строковому номеру
    def find_room(self, number):
        for room in self.rooms:
            if room.number == number:
                return room
        return None

    # Забронировать номер.
    def book_room(self, number):
        room = self.find_room(number)
        if room is None:
            return None                     
        if room.status == "занят":
            raise RoomAlreadyBookedError(f"Номер {number} уже занят!")
        room.status = "занят"
        return room

    # Освободить номер
    def release_room(self, number):
        room = self.find_room(number)
        if room is None:
            return None
        room.status = "свободен"
        return room

    # Найти все свободные номера
    def find_free_rooms(self):
        free = []
        for room in self.rooms:
            if room.status == "свободен":
                free.append(room)
        return free

    # Рассчитать стоимость проживания
    def calculate_cost(self, number, nights):
        room = self.find_room(number)
        if room is None:
            return None
        return room.price * nights

    # Превратить все номера в список словарей
    def to_list(self):
        result = []
        for room in self.rooms:
            result.append(room.to_dict())
        return result

    # Загрузить номера из списка словарей
    def load_from_list(self, data):
        self.rooms = []
        for d in data:
            self.rooms.append(Room.from_dict(d))
