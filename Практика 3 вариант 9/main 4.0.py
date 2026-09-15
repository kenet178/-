
#  БАЗОВЫЙ КЛАСС 

class Room:

    def __init__(self, nomer, cena):
        self.nomer = nomer          
        self.tip = "Базовый"        
        self.cena = cena           
        self._zabronirovan = False  

    @property
    def cena(self):
        return self._cena

    @cena.setter
    def cena(self, znachenie):
        if znachenie < 0:
            print("Ошибка: цена не может быть отрицательной. Ставлю 0.")
            self._cena = 0
        else:
            self._cena = znachenie

    @property
    def zabronirovan(self):
        return self._zabronirovan

    # Метод: бронирование
    def zabronirovat(self):
        if self._zabronirovan:
            print(f"Номер {self.nomer} уже забронирован.")
            return False
        self._zabronirovan = True
        print(f"Номер {self.nomer} успешно забронирован.")
        return True

    # Метод: освобождение
    def osvobodit(self):
        if not self._zabronirovan:
            print(f"Номер {self.nomer} и так свободен.")
            return False
        self._zabronirovan = False
        print(f"Номер {self.nomer} освобождён.")
        return True

    # Метод: расчёт стоимости проживания
    def rasschitat_stoimost(self, dni):
        return self.cena * dni

    # Метод: информация о номере в виде строки
    def poluchit_info(self):
        if self._zabronirovan:
            status = "занят"
        else:
            status = "свободен"
        return f"Номер {self.nomer} | {self.tip} | {self.cena} руб/ночь | {status}"


# НАСЛЕДНИКИ

class StandardRoom(Room):
    

    def __init__(self, nomer, cena):
        super().__init__(nomer, cena) 
        self.tip = "Стандарт"


class LuxuryRoom(Room):
    

    def __init__(self, nomer, cena, koefficient=1.5):
        super().__init__(nomer, cena)
        self.tip = "Люкс"
        self.koefficient = koefficient  

    def rasschitat_stoimost(self, dni):
        return self.cena * dni * self.koefficient

    def poluchit_info(self):
        bazovaya_info = super().poluchit_info()   
        return bazovaya_info + f" | x{self.koefficient}, завтрак включён"


# КЛАСС-КОНТЕЙНЕР 

class Hotel:
   

    def __init__(self, nazvanie):
        self.nazvanie = nazvanie
        self.nomera = []  

    # Добавить номер
    def dobavit_nomer(self, komnata):
        self.nomera.append(komnata)

    def naiti_nomer(self, nomer):
        for komnata in self.nomera:
            if komnata.nomer == nomer:
                return komnata
        return None

    # Показать номера
    def pokazat_vse(self):
        if len(self.nomera) == 0:
            print("В гостинице пока нет номеров.")
            return
        print()
        print(f"НОМЕРА ГОСТИНИЦЫ '{self.nazvanie}'")
        print("-" * 30)
        for komnata in self.nomera:
            print(komnata.poluchit_info())
        print()

    # Статистика по гостинице
    def statistika(self):
        vsego = len(self.nomera)
        zanyato = 0
        for komnata in self.nomera:
            if komnata.zabronirovan:
                zanyato = zanyato + 1
        svobodno = vsego - zanyato
        print()
        print("СТАТИСТИКА")
        print("---------")
        print(f"Всего номеров: {vsego}")
        print(f"Занято: {zanyato}")
        print(f"Свободно: {svobodno}")
        print()


# ПРОВЕРКА ВВОДА 

# Ввод непустой строки
def vvesti_stroku(soobshenie):
    stroka = input(soobshenie).strip()
    while stroka == "":
        print("Ошибка! Значение не может быть пустым.")
        stroka = input(soobshenie).strip()
    return stroka


# Ввод целого неотрицательного числа
def vvesti_chislo(soobshenie):
    stroka = input(soobshenie).strip()
    while not stroka.isdigit():
        print("Ошибка! Введите целое число не меньше нуля.")
        stroka = input(soobshenie).strip()
    return int(stroka)


# МЕНЮ 

def pokazat_menu():
    print("===== МЕНЮ =====")
    print("1. Создать номер")
    print("2. Показать все номера")
    print("3. Забронировать номер")
    print("4. Освободить номер")
    print("5. Статистика")
    print("0. Выход")


def main():
    hotel = Hotel("Уют")  

    while True:
        pokazat_menu()
        vybor = input("Выберите пункт: ").strip()

        if vybor == "1":
            # Создание номера
            print("Тип номера: 1 - Стандарт, 2 - Люкс")
            tip = input("Ваш выбор: ").strip()
            nomer = vvesti_stroku("Номер комнаты (например 101): ")
            if hotel.naiti_nomer(nomer) is not None:
                print("Такой номер уже существует.")
            else:
                cena = vvesti_chislo("Цена за ночь (руб): ")
                if tip == "1":
                    komnata = StandardRoom(nomer, cena)   
                    hotel.dobavit_nomer(komnata)
                    print("Стандартный номер создан.")
                elif tip == "2":
                    komnata = LuxuryRoom(nomer, cena)
                    hotel.dobavit_nomer(komnata)
                    print("Люкс создан.")
                else:
                    print("Неизвестный тип номера.")

        elif vybor == "2":
            hotel.pokazat_vse()

        elif vybor == "3":
            nomer = vvesti_stroku("Номер для брони: ")
            komnata = hotel.naiti_nomer(nomer)
            if komnata is None:
                print("Такого номера нет.")
            else:
                if komnata.zabronirovat():   
                    dni = vvesti_chislo("На сколько ночей? ")
                    stoimost = komnata.rasschitat_stoimost(dni)
                    print(f"Стоимость проживания: {stoimost} руб")

        elif vybor == "4":
            nomer = vvesti_stroku("Номер для освобождения: ")
            komnata = hotel.naiti_nomer(nomer)
            if komnata is None:
                print("Такого номера нет.")
            else:
                komnata.osvobodit()

        elif vybor == "5":
            hotel.statistika()

        elif vybor == "0":
            print("Выход из программы. До свидания!")
            break

        else:
            print("Нет такого пункта меню, попробуйте снова.")


if __name__ == "__main__":
    main()
