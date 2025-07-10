# CSV CLI Tool

CLI-программа для обработки CSV-файлов:
- Путь к файлу ('--file')
- Фильтрация данных по условию (`--where`)
- Агрегация значений (`--aggregate`)

main.png - Пример работы программы
test.png - Тест программы

## Установка и запуск

### Установка зависимостей

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
