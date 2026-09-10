# Проверки ввода

def eto_celoe_polozhitelnoe(stroka):
    if stroka.isdigit():        
        if int(stroka) > 0:     
            return True
    return False


def eto_polozhitelnoe_chislo(stroka):
    bez_tochki = stroka.replace(".", "", 1)
    if bez_tochki.isdigit():        
        if float(stroka) > 0:       
            return True
    return False


def vvesti_celoe(soobshenie):
    stroka = input(soobshenie).strip()     
    while not eto_celoe_polozhitelnoe(stroka):
        print("Ошибка! Нужно целое число больше нуля.")
        stroka = input(soobshenie).strip()
    return int(stroka)


def vvesti_summu(soobshenie):
    stroka = input(soobshenie).strip()
    while not eto_polozhitelnoe_chislo(stroka):
        print("Ошибка! Сумма должна быть положительным числом.")
        stroka = input(soobshenie).strip()
    return float(stroka)


# Вычисления

def poschitat_summu(pokupki):
    itog = 0
    for cena in pokupki:
        itog = itog + cena
    return itog


def naiti_maksimum(pokupki):
    maksimum = pokupki[0]           
    for cena in pokupki:
        if cena > maksimum:
            maksimum = cena
    return maksimum


def naiti_minimum(pokupki):
    minimum = pokupki[0]            
    for cena in pokupki:
        if cena < minimum:
            minimum = cena
    return minimum


def kolichestvo_vyshe_srednego(pokupki, srednee):
    schetchik = 0
    for cena in pokupki:
        if cena > srednee:
            schetchik = schetchik + 1
    return schetchik


def kolichestvo_nizhe_srednego(pokupki, srednee):
    schetchik = 0
    for cena in pokupki:
        if cena < srednee:
            schetchik = schetchik + 1
    return schetchik


def podschet_po_kategoriyam(pokupki):
    do_500 = 0                  
    ot_500_do_1000 = 0          
    bolshe_1000 = 0            

    for cena in pokupki:
        if cena < 500:
            do_500 = do_500 + 1
        elif cena <= 1000:
            ot_500_do_1000 = ot_500_do_1000 + 1
        else:
            bolshe_1000 = bolshe_1000 + 1

    return do_500, ot_500_do_1000, bolshe_1000


# Логика

def analiz_naboru():
    kolichestvo = vvesti_celoe("Сколько было покупок? ")

    pokupki = []
    for i in range(kolichestvo):
        summa = vvesti_summu(f"Введите сумму покупки №{i + 1}: ")
        pokupki.append(summa)

    obshaya_summa = poschitat_summu(pokupki)
    srednee = obshaya_summa / kolichestvo
    maksimum = naiti_maksimum(pokupki)
    minimum = naiti_minimum(pokupki)
    razmah = maksimum - minimum                     
    vyshe = kolichestvo_vyshe_srednego(pokupki, srednee)
    nizhe = kolichestvo_nizhe_srednego(pokupki, srednee)
    do_500, ot_500_do_1000, bolshe_1000 = podschet_po_kategoriyam(pokupki)

    print()
    print("РЕЗУЛЬТАТЫ АНАЛИЗА")
    print("-----------------")
    print(f"Количество покупок:   {kolichestvo}")
    print(f"Общая сумма расходов: {obshaya_summa} руб")
    print(f"Средний расход:       {round(srednee, 2)} руб")
    print(f"Максимальная покупка: {maksimum} руб")
    print(f"Минимальная покупка:  {minimum} руб")
    print(f"Разброс цен (макс-мин): {round(razmah, 2)} руб")
    print(f"Покупок выше среднего: {vyshe}")
    print(f"Покупок ниже среднего: {nizhe}")
    print()
    print("Покупки по категориям:")
    print(f"  до 500 руб:         {do_500}")
    print(f"  от 500 до 1000 руб: {ot_500_do_1000}")
    print(f"  больше 1000 руб:    {bolshe_1000}")
    print()


def pokazat_kategorii():
    print()
    print("Ценовые категории:")
    print("  1) до 500 руб")
    print("  2) от 500 до 1000 руб (границы включаются)")
    print("  3) больше 1000 руб")
    print()


def pokazat_menu():
    print("========== МЕНЮ ==========")
    print("1 - Анализ нового набора покупок")
    print("2 - Показать описание категорий")
    print("0 - Выход")
    print("==========================")


def main():
    print("Анализ личных расходов")
    print("----------------------")

    while True:
        pokazat_menu()
        vybor = input("Выберите пункт меню: ").strip()

        if vybor == "1":
            analiz_naboru()             
        elif vybor == "2":
            pokazat_kategorii()
        elif vybor == "0":
            print("Выход из программы. До свидания!")
            break                       
        else:
            print("Нет такого пункта меню, попробуйте снова.")
            print()


if __name__ == "__main__":
    main()