from bs4 import BeautifulSoup #Импортируем класс BeautifulSoup из библиотеки bs4 для парсинга HTML
import json #Импортируем модуль json для работы с JSON-форматом (сохранение данных)

def parse_parties(html_file_path):
    """Парсит HTML-файл и извлекает данные о политических партиях"""
    
    try:
        # Открываем и читаем HTML-файл (без проверки существования через os.path)
        with open(html_file_path, 'r', encoding='utf-8') as file:
            soup = BeautifulSoup(file, 'html.parser')
        
        # Ищем раздел (тег <div>) со списком партий c атрибутом (id="section-765")
        parties_section = soup.find('div', {'id': 'section-765'})
        
        if not parties_section:
            print(" Раздел со списком партий не найден!")
            return []
        
        # Находим все элементы списка партий ( ищем все теги <li> )
        party_items = parties_section.find_all('li')
        
        parties = []
        
        for item in party_items:
            # Находим ссылку в элементе списка (ищем тег <a>)
            link = item.find('a')
            
            if link:
                # Извлекаем название партии
                name = link.get_text(strip=True)
                name = ' '.join(name.split())  # Убираем множественные пробелы
                
                # Извлекаем ссылку
                href = link.get('href', '')
                
                # Обрабатываем ссылку
                if href:
                    # Делаем ссылку абсолютной, если она относительная
                    if href.startswith('/'):
                        doc_url = f"https://minjust.gov.ru{href}"
                    else:
                        doc_url = href
                    
                    # Исправляем протокол (для безопасности)
                    doc_url = doc_url.replace('http://', 'https://')
                    
                    # Убираем лишние query-параметры
                    doc_url = doc_url.split('?')[0]
                else:
                    doc_url = None
                
                # Добавляем партию в список
                parties.append({
                    "name": name,
                    "doc_url": doc_url
                })
            else:
                # Если нет ссылки, но есть текст
                text = item.get_text(strip=True)
                if text:
                    parties.append({
                        "name": text,
                        "doc_url": None
                    })
        
        return parties
    
    except FileNotFoundError:
        print(f" Файл {html_file_path} не найден!")
        return []
    except Exception as e:
        print(f" Ошибка при парсинге: {e}")
        return []

def print_results(parties):
    """Выводит результаты в консоль"""
    print(f"\n Найдено партий: {len(parties)}\n")
    print("=" * 80)
    
    for i, party in enumerate(parties, 1): #нумерация с 1
        print(f"{i}. {party['name']}")
        print(f"    Документ: {party['doc_url'] or 'Нет документа'}") #если doc_url равен None, выводим "Нет документа"
        print("-" * 80)

def main():
    # Указываем путь к вашему HTML-файлу
    html_file = "politicheskie-partii.html"
    
    # Парсим данные
    print(f" Парсим файл: {html_file}")
    parties = parse_parties(html_file)
    
    if parties:
        # Выводим результаты
        print_results(parties)
        
        # Сохраняем в JSON (опционально)
        try:
            with open('parties.json', 'w', encoding='utf-8') as f:
                json.dump(parties, f, ensure_ascii=False, indent=2)
            print(f"\n Данные сохранены в parties.json")
        except Exception as e:
            print(f"\nНе удалось сохранить в JSON: {e}")
        
        # Пример использования данных
        print(f"\n Структура данных Python:")
        print(f"   Тип данных: {type(parties)} (список)")
        print(f"   Количество элементов: {len(parties)}")
        print(f"\n   Первый элемент:")
        print(f"   Тип: {type(parties[0])} (словарь)")
        print(f"   Ключи: {list(parties[0].keys())}")
        print(f"   Значения: {list(parties[0].values())}")
    else:
        print(" Не удалось извлечь данные о партиях")

if __name__ == "__main__":
    main()
