
# Ввод непустой строки
def vvesti_stroku(soobshenie):
    stroka = input(soobshenie).strip()      
    while stroka == "":                      
        print("Ошибка! Значение не может быть пустым.")
        stroka = input(soobshenie).strip()
    return stroka

def vvesti_chislo(soobshenie):
    stroka = input(soobshenie).strip()
    while not stroka.isdigit():
        print("Ошибка! Введите целое число не меньше нуля.")
        stroka = input(soobshenie).strip()
    return int(stroka)


# ОСНОВНЫЕ ФУНКЦИИ
# Поиск тренировок заданного типа
def naiti_po_tipu(trenirovki, tip):
    naydeno = [t for t in trenirovki if t["type"].lower() == tip.lower()]
    return naydeno


def filtr_po_dlitelnosti(trenirovki, min_dlit, max_dlit):
    naydeno = [t for t in trenirovki if min_dlit <= t["duration"] <= max_dlit]
    return naydeno


# Статистика
def poschitat_statistiku(trenirovki):
    obshee_vremya = sum([t["duration"] for t in trenirovki])

    vsego_kalorij = sum([t["calories"] for t in trenirovki])
    kolichestvo = len(trenirovki)                  
    sredniy_rashod = vsego_kalorij / kolichestvo  
    return obshee_vremya, sredniy_rashod


# Список уникальных типов тренировок
def poluchit_unikalnye_tipy(trenirovki):
    tipy = set()
    for t in trenirovki:
        tipy.add(t["type"])
    return list(tipy)   


def vzyat_dlitelnost(trenirovka):
    return trenirovka["duration"]


# Сортировка по возрастанию
def sortirovka_po_dlitelnosti(trenirovki):
    otsortirovano = sorted(trenirovki, key=vzyat_dlitelnost)
    return otsortirovano


# УДАЛЕНИЕ

# Удаление тренировки по номеру
def udalit_po_nomeru(trenirovki, nomer):
    if 1 <= nomer <= len(trenirovki):
        udalennaya = trenirovki.pop(nomer - 1)  
        return udalennaya
    return None  


# Удаление тренировки по названию
def udalit_po_nazvaniyu(trenirovki, nazvanie):
    for i in range(len(trenirovki)):
        if trenirovki[i]["name"].lower() == nazvanie.lower():
            return trenirovki.pop(i)   
    return None   


# ВЫВОД 

# Показать список тренировок на экране
def pokazat_vse(trenirovki):
    if len(trenirovki) == 0:
        print("Список тренировок пуст.")
        return
    print()
    print("СПИСОК ТРЕНИРОВОК")
    print("-----------------")
    nomer = 1
    for t in trenirovki:
        print(f"{nomer}. {t['name']} | тип: {t['type']} | "
              f"{t['duration']} мин | {t['calories']} ккал")
        nomer = nomer + 1
    print()


# Добавить тренировку
def dobavit_trenirovku(trenirovki):
    name = vvesti_stroku("Название тренировки: ")
    tip = vvesti_stroku("Тип тренировки: ")
    duration = vvesti_chislo("Продолжительность (мин): ")
    calories = vvesti_chislo("Сожжённые калории: ")
    trenirovka = {"name": name, "type": tip, "duration": duration, "calories": calories}
    trenirovki.append(trenirovka)  
    print("Тренировка добавлена!")


# меню
def pokazat_menu():
    print("===== МЕНЮ =====")
    print("1. Добавить тренировку")
    print("2. Показать все тренировки")
    print("3. Найти тренировки по типу")
    print("4. Фильтрация по продолжительности")
    print("5. Сортировка по продолжительности")
    print("6. Статистика")
    print("7. Уникальные типы тренировок")
    print("8. Удалить тренировку")
    print("0. Выход")


# ГЛАВНАЯ ФУНКЦИЯ

def main():
    trenirovki = []  

    while True:
        pokazat_menu()
        vybor = input("Выберите пункт: ").strip()

        if vybor == "1":
            dobavit_trenirovku(trenirovki)

        elif vybor == "2":
            pokazat_vse(trenirovki)

        elif vybor == "3":
            if len(trenirovki) == 0:
                print("Сначала добавьте тренировки.")
            else:
                tip = vvesti_stroku("Введите тип для поиска: ")
                naydeno = naiti_po_tipu(trenirovki, tip)
                if len(naydeno) == 0:
                    print("Тренировки такого типа не найдены.")
                else:
                    pokazat_vse(naydeno)

        elif vybor == "4":
            if len(trenirovki) == 0:
                print("Сначала добавьте тренировки.")
            else:
                min_dlit = vvesti_chislo("Минимальная продолжительность (мин): ")
                max_dlit = vvesti_chislo("Максимальная продолжительность (мин): ")
                naydeno = filtr_po_dlitelnosti(trenirovki, min_dlit, max_dlit)
                if len(naydeno) == 0:
                    print("Ничего не найдено в этом диапазоне.")
                else:
                    pokazat_vse(naydeno)

        elif vybor == "5":
            if len(trenirovki) == 0:
                print("Сначала добавьте тренировки.")
            else:
                otsortirovano = sortirovka_po_dlitelnosti(trenirovki)
                pokazat_vse(otsortirovano)

        elif vybor == "6":
            if len(trenirovki) == 0:
                print("Сначала добавьте тренировки.")
            else:
                obshee_vremya, sredniy_rashod = poschitat_statistiku(trenirovki)
                print()
                print("СТАТИСТИКА")
                print("---------")
                print(f"Всего тренировок: {len(trenirovki)}")
                print(f"Общее время: {obshee_vremya} мин")
                print(f"Средний расход калорий: {round(sredniy_rashod, 2)} ккал")
                print()

        elif vybor == "7":
            if len(trenirovki) == 0:
                print("Сначала добавьте тренировки.")
            else:
                tipy = poluchit_unikalnye_tipy(trenirovki)
                print()
                print("Уникальные типы тренировок:")
                for tip in tipy:
                    print(f"  - {tip}")
                print()

        elif vybor == "8":
            if len(trenirovki) == 0:
                print("Список пуст, удалять нечего.")
            else:
                pokazat_vse(trenirovki)
                print("Удалить: 1 - по номеру, 2 - по названию")
                sposob = input("Ваш выбор: ").strip()
                if sposob == "1":
                    nomer = vvesti_chislo("Введите номер тренировки: ")
                    udalennaya = udalit_po_nomeru(trenirovki, nomer)
                elif sposob == "2":
                    nazvanie = vvesti_stroku("Введите название: ")
                    udalennaya = udalit_po_nazvaniyu(trenirovki, nazvanie)
                else:
                    udalennaya = None
                    print("Неизвестный способ удаления.")

                if udalennaya is not None:
                    print(f"Удалена тренировка: {udalennaya['name']}")
                elif sposob == "1" or sposob == "2":
                    print("Тренировка не найдена.")

        elif vybor == "0":
            print("Выход из программы. До свидания!")
            break

        else:
            print("Нет такого пункта меню, попробуйте снова.")


if __name__ == "__main__":
    main()
