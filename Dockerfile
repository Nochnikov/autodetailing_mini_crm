# Используем официальный образ Python
FROM python:3.11-slim-bullseye

# Устанавливаем зависимости
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файл зависимостей и устанавливаем их
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt



# Копируем весь проект в рабочую директорию
COPY . /app/

# Устанавливаем порт, который будет использоваться
EXPOSE 8000

COPY ./entrypoint.dev.sh /entrypoint.dev.sh
RUN chmod +x /entrypoint.dev.sh

CMD ["/entrypoint.dev.sh"]