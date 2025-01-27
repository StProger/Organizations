# Инструкция по запуску

1. Клонировать репозиторий:

   ```bash
   git clone https://github.com/StProger/Organizations.git

2. Запуск приложения с помощью утилиты make:

    ```bash
    make app

3. После запуска API будет доступно по url http://localhost:8000/api/docs (или http://0.0.0.0:8000/api/docs)

4. Остановка контейнеров:
    ```bash
    make app-down

5. Просмотр логов:  
    ```bash
    make app-logs
