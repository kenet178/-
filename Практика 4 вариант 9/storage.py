# Модуль для работы с файлами: сохранение и загрузка данных

import json   
import csv    


# Сохранить список словарей в JSON-файл
def save_to_json(data, filename):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


# Загрузить список словарей из JSON-файла
def load_from_json(filename):
    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)


# Экспортировать список словарей в CSV-файл
def export_to_csv(data, filename):
    if len(data) == 0:      
        return
    
    polya = data[0].keys()
    with open(filename, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=polya)
        writer.writeheader()      
        writer.writerows(data)    
