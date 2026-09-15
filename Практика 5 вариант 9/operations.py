from functools import reduce  


# ФУНКЦИИ ВЫСШЕГО ПОРЯДКА

# Фильтрация
def filter_objects(objects, predicate):
    return list(filter(predicate, objects))


# Преобразование
def transform_objects(objects, operation):
    return list(map(operation, objects))


# Сортировка
def sort_objects(objects, key_function):
    return sorted(objects, key=key_function)


# КОНКРЕТНЫЕ ОПЕРАЦИИ ДЛЯ НОМЕРОВ
# Свободные номера (filter + lambda)
def free_rooms(rooms):
    return filter_objects(rooms, lambda room: room.is_free())


# Список номеров комнат (map + lambda)
def room_numbers(rooms):
    return transform_objects(rooms, lambda room: room.number)


# Сортировка по стоимости (sorted)
def rooms_by_price(rooms):
    return sort_objects(rooms, lambda room: room.price)


# Самый дорогой номер (reduce)
def most_expensive_room(rooms):
    if len(rooms) == 0:
        return None
    return reduce(lambda a, b: a if a.price >= b.price else b, rooms)


# Есть ли хотя бы один свободный номер (any)
def has_free_room(rooms):
    return any(room.is_free() for room in rooms)


# Все ли номера дороже заданной цены (all)
def all_more_expensive(rooms, min_price):
    return all(room.price > min_price for room in rooms)


# Общая стоимость всех номеров за ночь (comprehension + sum)
def total_price(rooms):
    return sum([room.price for room in rooms])
