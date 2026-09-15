# Модуль с моделью данных


class Room:

    def __init__(self, number, category, price, capacity, status="свободен"):
        self.number = number        
        self.category = category    
        self.price = price          
        self.capacity = capacity    
        self.status = status        

    def to_dict(self):
        return {
            "number": self.number,
            "category": self.category,
            "price": self.price,
            "capacity": self.capacity,
            "status": self.status,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["number"],
            data["category"],
            data["price"],
            data["capacity"],
            data["status"],
        )

    def __str__(self):
        return (f"Номер {self.number} | {self.category} | "
                f"{self.price} руб/ночь | мест: {self.capacity} | {self.status}")
