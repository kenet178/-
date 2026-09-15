# ГЕНЕРАТОР

# Генератор номеров заданной категории
def rooms_by_category(rooms, category):
    for room in rooms:
        if room.category == category:
            yield room   


# Генератор только свободных номеров
def free_rooms_generator(rooms):
    for room in rooms:
        if room.is_free():
            yield room


# СОБСТВЕННЫЙ ИТЕРАТОР

class RoomIterator:
    def __init__(self, rooms):
        self.rooms = rooms   
        self.index = 0       

    def __iter__(self):
        return self

    def __next__(self):
        if self.index >= len(self.rooms):
            raise StopIteration          
        result = self.rooms[self.index]  
        self.index = self.index + 1      
        return result
