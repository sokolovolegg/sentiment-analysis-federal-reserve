import requests
from bs4 import BeautifulSoup
import os
import time  # Import the time module

# Генерация списка всех дат для минут (например, для 2024 года)
years = list(range(2006, 1999, -1))  # Диапазон с 2024 по 2000 (включительно)
months = list(range(1, 13))  # Все месяцы от 1 до 12
days = list(range(1, 32))  # Все возможные дни от 1 до 31

# Функция для формирования ссылки
def generate_url(year, month, day):
    # Форматируем месяц и день с ведущими нулями
    month_str = str(month).zfill(2)
    day_str = str(day).zfill(2)
    return f"https://www.federalreserve.gov/fomc/minutes/{year}{month_str}{day_str}.htm"

# Создаем папку для хранения текстов
os.makedirs("fomc_minutes", exist_ok=True)

# Загружаем и обрабатываем каждую страницу для всех комбинаций
for year in years:
    for month in months:
        for day in days:
            url = generate_url(year, month, day)
            print(f"Пытаемся загрузить страницу: {url}")
            
            response = requests.get(url)
            if response.status_code != 200:
                print(f"Ошибка при загрузке страницы {url}: {response.status_code}")
                continue
            
            # Парсим HTML страницы
            soup = BeautifulSoup(response.text, "html.parser")
            
            # Извлекаем текст из документа
            text = soup.get_text(separator="\n", strip=True)
            
            # Имя файла для сохранения
            filename = url.split("/")[-1].replace(".htm", ".txt")  # Имя файла с текстом
            filepath = os.path.join("fomc_minutes", filename)
            
            # Сохраняем текст в .txt файл
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(text)
            
            print(f"Сохранено: {filename}")
            
            # Добавляем задержку между запросами
            time.sleep(1)  # Задержка в 1 секунду
