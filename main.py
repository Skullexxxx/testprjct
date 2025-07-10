import argparse  # Библиотека для обработки аргументов командной строки
import csv       # Модуль для работы с CSV-файлами
import sys       # Для управления потоком ошибок и завершения программы
from tabulate import tabulate  # Для красивого вывода таблиц в консоль


# Функция читает CSV-файл и возвращает данные в виде списка словарей
def read_csv(file_path):
    try:
        # Пытаемся открыть файл и прочитать его построчно
        with open(file_path, newline='', encoding='utf-8') as f:
            return list(csv.DictReader(f))  # Читаем файл как словари
    except FileNotFoundError:
        print(f"Ошибка: файл {file_path} не найден!", file=sys.stderr)
        sys.exit(1)  # Завершаем программу с кодом ошибки
    except Exception as e:
        # Обрабатываем другие ошибки чтения файла
        print(f"Ошибка при чтении файла: {e}", file=sys.stderr)
        sys.exit(1)


# Функция разбирает строку условия фильтрации на 3 части: колонку, оператор и значение
def parse_condition(cond):
    ops = ('=', '>', '<')  # Возможные операторы
    for op in ops:
        if op in cond:
            parts = cond.split(op)
            if len(parts) == 2:
                # Возвращаем колонку, оператор и значение
                return parts[0].strip(), op, parts[1].strip()
    # Если формат неправильный — выводим ошибку
    print(f"Ошибка: некорректное условие '{cond}'", file=sys.stderr)
    sys.exit(1)


# Функция фильтрует данные на основе условия
def filter_data(data, condition):
    if not condition:
        return data  # Если нет условия — возвращаем все данные

    col, op, val = parse_condition(condition)  # Получаем части условия
    result = []

    for row in data:
        try:
            if op == '=' and str(row[col]) == val:
                result.append(row)  # Добавляем подходящую строку
            elif op in ('>', '<'):
                row_val = float(row[col])
                cond_val = float(val)
                if op == '>' and row_val > cond_val:
                    result.append(row)
                elif op == '<' and row_val < cond_val:
                    result.append(row)
        except (KeyError, ValueError):
            continue  # Пропускаем строки с ошибками

    return result


# Функция для агрегации данных по колонке (avg, min, max)
def aggregate_data(data, agg_condition):
    if not agg_condition:
        return None  # Если агрегации нет — возвращаем None

    try:
        col, func = agg_condition.split('=')  # Разделяем по знаку '='
        col = col.strip()
        func = func.strip().lower()  # Приводим к нижнему регистру

        values = []
        for row in data:
            try:
                # Преобразуем значения колонки в числа
                values.append(float(row[col]))
            except (KeyError, ValueError):
                continue  # Пропускаем строки с ошибками

        if not values:
            return None  # Если нет значений — ничего не агрегируем

        # Выполняем нужную функцию
        if func == 'avg':
            res = sum(values) / len(values)
        elif func == 'min':
            res = min(values)
        elif func == 'max':
            res = max(values)
        else:
            # Если неизвестная агрегация — ошибка
            print(f"Ошибка: неизвестная агрегация '{func}'", file=sys.stderr)
            sys.exit(1)

        # Возвращаем результат в виде словаря
        return {'column': col, 'function': func, 'result': res}

    except Exception as e:
        # Общая ошибка при агрегации
        print(f"Ошибка в агрегации: {e}", file=sys.stderr)
        sys.exit(1)


# Эта функция объединяет все действия: чтение, фильтрацию и агрегацию
def process(file_path, where=None, aggregate=None):
    data = read_csv(file_path)  # Сначала читаем файл

    if where:
        data = filter_data(data, where)  # Применяем фильтр, если есть

    if aggregate:
        agg_result = aggregate_data(data, aggregate)  # Проводим агрегацию
        if agg_result:
            print(f"Агрегация '{aggregate}':")
            print(tabulate([agg_result], headers='keys', tablefmt='grid'))  # Печатаем результат
        else:
            print("Нет данных для агрегации", file=sys.stderr)
    else:
        if not data:
            print("Нет данных для отображения", file=sys.stderr)
            return
        # Выводим таблицу с результатами
        print(tabulate(data, headers='keys', tablefmt='grid'))


# Точка входа, если скрипт запущен напрямую
def main():
    # Создаём парсер аргументов командной строки
    parser = argparse.ArgumentParser(description='Обработка CSV: фильтрация и агрегация')
    parser.add_argument('-f', '--file', required=True, help='Путь к CSV файлу')
    parser.add_argument('--where', help='Фильтрация (пример: поле=значение)')
    parser.add_argument('--aggregate', help='Агрегация (пример: поле=avg/min/max)')

    args = parser.parse_args()  # Считываем аргументы

    # Передаём параметры в основную функцию
    process(args.file, args.where, args.aggregate)


# Проверяем, что файл запущен как основной
if __name__ == '__main__':
    main()