# Собственные декораторы

import time
from functools import wraps


# Декоратор №1 — журналирование вызова функции
def log_call(func):
    @wraps(func)   # wraps сохраняет имя и docstring исходной функции
    def wrapper(*args, **kwargs):
        print(f"[LOG] вызван {func.__name__}()")
        result = func(*args, **kwargs)
        print(f"[LOG] {func.__name__}() завершён")
        return result
    return wrapper


# Декоратор №2 — измерение времени выполнения
def measure_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"[PERFORMANCE] {func.__name__}: {elapsed:.6f} sec")
        return result
    return wrapper


# Декоратор №3 — с параметром: разрешает операцию только при нужном статусе рейса.
# Оборачиваемая функция должна принимать рейс первым аргументом.
def require_status(status):
    def decorator(func):
        @wraps(func)
        def wrapper(flight, *args, **kwargs):
            if flight.status != status:
                raise ValueError(
                    f"Операция недоступна: статус рейса '{flight.status.value}', "
                    f"нужен '{status.value}'"
                )
            return func(flight, *args, **kwargs)
        return wrapper
    return decorator
