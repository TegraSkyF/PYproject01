# Sales Data Analyzer

A comprehensive web application for analyzing sales data with key metrics, visualization, and anomaly detection.

## Features

- **Dashboard**: Interactive dashboard with key metrics and visualizations
- **Data Upload**: Support for Excel files (.xlsx, .xls)
- **Anomaly Detection**: Statistical detection of outliers in sales data
- **Visualization**: Interactive charts and correlation matrices
- **Help Section**: Comprehensive documentation and guidance

## Requirements

- Python 3.8+
- Streamlit
- Pandas
- Plotly
- NumPy
- OpenPyXL
- XLRD

## Installation

1. Clone or download this repository
2. Navigate to the project directory
3. Create and activate a virtual environment:
   ```
   python -m venv venv
   venv\Scripts\activate  # On Windows
   source venv/bin/activate  # On macOS/Linux
   ```
4. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Usage

### Quick Start
Run the provided batch script (on Windows):
```
start_app.bat
```

### Manual Start
1. Activate your virtual environment:
   ```
   venv\Scripts\activate  # On Windows
   source venv/bin/activate  # On macOS/Linux
   ```
2. Run the Streamlit application:
   ```
   streamlit run sales_analyzer_app.py
   ```
3. Open your browser and go to `http://localhost:8501`

## File Format

The application accepts Excel files (.xlsx or .xls) with tabular data. Recommended columns include:
- Date/Time column (for time series analysis)
- Numeric columns (for sales figures, quantities, prices, etc.)
- Categorical columns (for products, regions, categories, etc.)

## Pages

1. **Dashboard**: Main analytics dashboard with key metrics and visualizations
2. **Data Upload**: Page to upload your sales data file
3. **Anomaly Detection**: Identifies outliers in your data using statistical methods
4. **Help**: Documentation and usage instructions

## Anomaly Detection Method

The application uses the Interquartile Range (IQR) method to detect anomalies:
- Calculate Q1 (25th percentile) and Q3 (75th percentile)
- Compute IQR = Q3 - Q1
- Define bounds: Lower = Q1 - 1.5×IQR, Upper = Q3 + 1.5×IQR
- Values outside these bounds are considered anomalies

## Troubleshooting

If you encounter issues:
- Verify the file is a valid Excel file (.xlsx or .xls)
- Check that the file isn't password protected
- Ensure the file size isn't too large (recommended < 100MB)
- Make sure the file contains tabular data

Анализатор данных о продажах
Комплексное веб-приложение для анализа данных о продажах с ключевыми показателями, визуализацией и обнаружением аномалий.

Особенности
Информационная панель: Интерактивная информационная панель с ключевыми показателями и визуализациями
Загрузка данных: Поддержка файлов Excel (.xlsx, .xls)
Обнаружение аномалий: Статистическое выявление отклонений в данных о продажах
Визуализация: интерактивные диаграммы и корреляционные матрицы
Раздел справки: Подробная документация и рекомендации
Требования
Python 3.8+
Streamlit
Панды
Плотнее
NumPy
OpenPyXL
XLRD
Установка
Клонировать или загрузить этот репозиторий
Перейдите в каталог проекта
Создайте и активируйте виртуальную среду:
python -m venv venv
venv\Scripts\activate # В
исходном коде Windows venv/bin/activate # В macOS/Linux
Установите необходимые пакеты:
pip install -r requirements.txt
Использование
быстрый старт
Запустите предоставленный пакетный скрипт (в Windows):

start_app.bat
Запуск вручную
Активируйте свою виртуальную среду:
venv\Scripts\activate # В
исходном коде Windows venv/bin/activate # В macOS/Linux
Запустите приложение Streamlit:
streamlit run sales_analyzer_app.py
Откройте свой браузер и перейдите к разделу http://localhost:8501
Формат файла
Приложение поддерживает файлы Excel (.xlsx или .xls) с табличными данными. Рекомендуемые столбцы включают:

Столбец даты/времени (для анализа временных рядов)
Числовые столбцы (для данных о продажах, количествах, ценах и т.д.)
Категориальные столбцы (для продуктов, регионов, категорий и т.д.)
Страницы
Панель мониторинга: Главная аналитическая панель с ключевыми показателями и визуализациями
Загрузка данных: Страница для загрузки файла с данными о продажах
Обнаружение аномалий: Выявляет отклонения в ваших данных с помощью статистических методов
Справка: Документация и инструкции по использованию
Способ обнаружения аномалий
Приложение использует метод межквартильного разбиения (IQR) для обнаружения аномалий:

Вычисляет Q1 (25-й процентиль) и Q3 (75-й процентиль)
Вычисляет IQR = Q3 - Q1
Определите границы: Нижняя = Q1 - 1,5×IQR, Верхняя = Q3 + 1,5×IQR
Значения, выходящие за эти границы, считаются аномалиями
Диагностика
Если вы столкнетесь с проблемами:

Убедитесь, что файл является допустимым файлом Excel (.xlsx или .xls)
Убедитесь, что файл не защищен паролем
Убедитесь, что размер файла не слишком большой (рекомендуется < 100 МБ)
Убедитесь, что файл содержит табличные данные
