class Room:
    def __init__(self, number, category, price, capacity, status="свободен"):
        self.number = number        
        self.category = category   
        self.price = price          
        self.capacity = capacity   
        self.status = status       

    # Свободен номер
    def is_free(self):
        return self.status == "свободен"

    def __str__(self):
        return (f"Номер {self.number} | {self.category} | "
                f"{self.price} руб/ночь | мест: {self.capacity} | {self.status}")


class StandardRoom(Room):
    def __init__(self, number, price, capacity, status="свободен"):
        super().__init__(number, "Стандарт", price, capacity, status)


class LuxuryRoom(Room):
    def __init__(self, number, price, capacity, status="свободен"):
        super().__init__(number, "Люкс", price, capacity, status)
