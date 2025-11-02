"""
Скрипт для тестирования API
Запустите: python test_api.py
"""
import requests
import json
import time

API_BASE = "http://localhost:8000/api"

def print_response(title, response):
    """Красиво выводит ответ"""
    print(f"\n{'='*50}")
    print(f"{title}")
    print(f"{'='*50}")
    print(f"Status: {response.status_code}")
    try:
        data = response.json()
        print(json.dumps(data, indent=2, ensure_ascii=False))
    except:
        print(response.text)
    print()

def test_health():
    """Проверка здоровья сервера"""
    print("Проверка работы сервера...")
    try:
        response = requests.get(f"{API_BASE.replace('/api', '')}/health", timeout=2)
        print_response("Health Check", response)
        return response.status_code == 200
    except requests.exceptions.ConnectionError:
        print("[ERROR] Сервер не запущен! Запустите: python main.py")
        return False
    except Exception as e:
        print(f"[ERROR] Ошибка: {e}")
        return False

def test_create_notification():
    """Создание тестового уведомления"""
    print("Создание тестового уведомления...")
    response = requests.get(f"{API_BASE}/webhooks/airtable/test")  # GET, а не POST
    print_response("Создание уведомления", response)
    return response.status_code in [200, 201]

def test_get_notifications():
    """Получение списка уведомлений"""
    print("Получение списка уведомлений...")
    response = requests.get(f"{API_BASE}/notifications")
    print_response("Список уведомлений", response)
    return response.status_code == 200

def test_get_stats():
    """Получение статистики"""
    print("Получение статистики...")
    response = requests.get(f"{API_BASE}/stats")
    print_response("Статистика", response)
    return response.status_code == 200

def test_create_custom_notification():
    """Создание кастомного уведомления"""
    print("Создание кастомного уведомления...")
    data = {
        "type": "file_upload",
        "title": "Загрузка файла",
        "description": "Загружен файл test_report.xlsx в таблицу Документы",
        "user_id": "manager_test",
        "user_name": "Тестовый менеджер",
        "source": "airtable",
        "details": {
            "table_name": "Документы",
            "file_type": "XLSX"
        }
    }
    response = requests.post(
        f"{API_BASE}/notifications",
        json=data
    )
    print_response("Создание кастомного уведомления", response)
    return response.status_code in [200, 201]

def main():
    print("[*] Начинаем тестирование API...")
    print("Убедитесь, что сервер запущен (python main.py)")
    print()
    
    # Ждем немного для запуска сервера
    time.sleep(1)
    
    # Тесты
    if not test_health():
        return
    
    test_create_notification()
    test_create_custom_notification()
    test_get_notifications()
    test_get_stats()
    
    print("\n[OK] Тестирование завершено!")
    print("\nОткройте в браузере:")
    print("  - Swagger UI: http://localhost:8000/docs")
    print("  - ReDoc: http://localhost:8000/redoc")
    print("  - Frontend: откройте index.html")

if __name__ == "__main__":
    main()

