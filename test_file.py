import json
import os
import time
from translate import Translator

def clear_terminal():
    """Очистка терминала"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_progress_bar(current, total, translated_count, skip_count, bar_length=40):
    """Вывод прогресс-бара и статистики"""
    progress = current / total
    arrow = '█' * int(round(bar_length * progress))
    spaces = ' ' * (bar_length - len(arrow))
    
    percent = round(progress * 100, 1)
    
    print(f"Прогресс: [{arrow}{spaces}] {percent}% ({current}/{total})")
    print(f"Успешно переведено: {translated_count}")
    print(f"Пропущено слов: {skip_count}")
    print(f"Текущее слово: {current}/{total}")
    print("-" * 50)

def translate_words():
    # Загрузка английских слов
    with open('data/engword.json', 'r', encoding='utf-8') as f:
        eng_words = json.load(f)
    
    # Инициализация переводчика
    translator = Translator(to_lang="ru")
    
    translated_words = []
    translated_count = 0
    skip_count = 0
    total_words = len(eng_words)
    
    print("Начинаем перевод...")
    time.sleep(2)
    
    for i, word in enumerate(eng_words):
        # Очищаем терминал и обновляем статистику
        clear_terminal()
        print("=== ПЕРЕВОД АНГЛИЙСКИХ СЛОВ ===")
        print_progress_bar(i, total_words, translated_count, skip_count)
        
        if len(word) < 2:  # Пропускаем слишком короткие слова
            skip_count += 1
            translated_words.append("")
            continue
            
        try:
            translation = translator.translate(word)
            
            # Проверяем условия пропуска
            if (not translation or 
                translation.lower() == word.lower() or 
                ' ' in translation or
                '-' in translation):
                
                skip_count += 1
                translated_words.append("")
            else:
                translated_count += 1
                translated_words.append(translation)
                
        except Exception:
            # При ошибке перевода пропускаем слово
            skip_count += 1
            translated_words.append("")
            continue
        
        # Небольшая задержка для избежания блокировки API
        time.sleep(0.1)
    
    # Финальное обновление
    clear_terminal()
    print("=== ПЕРЕВОД ЗАВЕРШЕН ===")
    print_progress_bar(total_words, total_words, translated_count, skip_count)
    
    # Сохранение результатов
    with open('data/rusword.json', 'w', encoding='utf-8') as f:
        json.dump(translated_words, f, ensure_ascii=False, indent=2)
    
    print(f"\nРезультаты сохранены в файл: rusword.json")
    print(f"Итоговая статистика:")
    print(f"  • Всего слов: {total_words}")
    print(f"  • Успешно переведено: {translated_count}")
    print(f"  • Пропущено: {skip_count}")
    print(f"  • Процент успеха: {(translated_count/total_words)*100:.1f}%")

if __name__ == "__main__":
    translate_words()