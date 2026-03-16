# send_query.py
import requests
import json

# --- адрес FastAPI сервера ---
API_URL = "http://89.179.146.97:5081"  # замените <IP_сервера> на реальный IP

# --- тело запроса ---
payload = {
    "text": "Какие требования к оперативной памяти?",
    "mode": "hybrid",
    "level": [0,1,2],
    "limit": 5,
    "use_summary": False
}

try:
    # --- отправляем POST-запрос ---
    response = requests.post(f"{API_URL}/search", json=payload, timeout=10)
    response.raise_for_status()  # вызовет исключение, если статус != 200

    # --- выводим результат ---
    result = response.json()
    print("=== Результаты поиска ===")
    for i, hit in enumerate(result["results"], start=1):
        print(f"{i}: {hit}")

    print("\n=== Собранный контекст ===")
    print(result["context"])

except requests.exceptions.RequestException as e:
    print(f"Ошибка при подключении к API: {e}")

# =========================================================
# 2️⃣ DB QUERY (по doc_id)
# =========================================================

db_payload = {
    "collection": "documents",  
    "filter": "doc_id == '9ed1ceef-6bf5-4c73-9ea2-fae560804c4e'",
    "limit": 15,
    "output_fields": ["id", "title", "source", "level"]
}

try:
    response = requests.post(f"{API_URL}/query", json=db_payload, timeout=10)
    response.raise_for_status()

    result = response.json()

    print("\n=== DB QUERY RESULT ===")
    print(f"Найдено {len(result['results'])} записей:\n")

    for row in result["results"]:
        print(row)

except requests.exceptions.RequestException as e:
    print(f"Ошибка при DB query: {e}")