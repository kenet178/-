# Собственный контекстный менеджер

import time


# Контекстный менеджер: журналирует начало/конец блока и измеряет время.
class OperationBlock:
    def __init__(self, name):
        self.name = name

    # __enter__ вызывается при входе в блок with
    def __enter__(self):
        print(f"[BLOCK] начало операции: {self.name}")
        self.start = time.perf_counter()
        return self

    # __exit__ вызывается при выходе из блока (даже при ошибке)
    def __exit__(self, exc_type, exc_value, traceback):
        elapsed = time.perf_counter() - self.start
        print(f"[BLOCK] конец операции: {self.name} ({elapsed:.6f} sec)")
        return False   # False = исключения не подавляем
