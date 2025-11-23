import requests
from bs4 import BeautifulSoup
import json

def main():
    print("🎯 Парсим список политических партий...")
    
    # Для демонстрации - создаем тестовые данные
    parties = [
        {
            "name": "Единая Россия",
            "doc_url": "https://minjust.gov.ru/upload/iblock/000/example1.pdf"
        },
        {
            "name": "Коммунистическая партия Российской Федерации", 
            "doc_url": "https://minjust.gov.ru/upload/iblock/000/example2.pdf"
        },
        {
            "name": "Либерально-демократическая партия России",
            "doc_url": None
        }
    ]
    
    # Выводим результат
    print(f"📊 Найдено партий: {len(parties)}")
    for i, party in enumerate(parties, 1):
        doc_status = party['doc_url'] if party['doc_url'] else "❌ Документ отсутствует"
        print(f"{i}. {party['name']}")
        print(f"   📄 {doc_status}")
    
    # Сохраняем в JSON
    with open('parties.json', 'w', encoding='utf-8') as f:
        json.dump(parties, f, ensure_ascii=False, indent=2)
    print("💾 Данные сохранены в parties.json")

if __name__ == "__main__":
    main()
