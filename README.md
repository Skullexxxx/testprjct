# CSV CLI Tool

CLI-программа для обработки CSV-файлов:
- Фильтрация данных по условию (`--where`)
- Агрегация значений (`--aggregate`)

## Установка и запуск

### Установка зависимостей

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt