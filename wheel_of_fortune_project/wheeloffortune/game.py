try:
    from wheeloffortune.file_handler import random_word_generator, save_records, get_high_scores, entry_records, update_record
    from wheeloffortune.decorators import log_errors
    from wheeloffortune.utils import display_word
except:
    from file_handler import random_word_generator, save_records, get_high_scores, entry_records, update_record
    from decorators import log_errors
    from utils import display_word
import time

all_words = list(random_word_generator())
total_words = len(all_words)

def set_difficulty():
    while True:
        print('Выберите уровень сложности:')
        print('1 - Легкий (7 жизней)')
        print('2 - Средний (5 жизней)')
        print('3 - Сложный (3 жизни)')
        choice = input('Ваш выбор: ').strip()
        if choice == '1':
            return 7, 'easy'
        elif choice == '2':
            return 5, 'medium'
        elif choice == '3':
            return 3, 'hard'
        else:
            print(' Пожалуйста, введите число от 1 до 3')

@log_errors
def play_game(player_name):
    used_words = set()
    lives, diff = set_difficulty()
    score = 0
    start_time = time.time()

    word_generator = random_word_generator()

    for word in word_generator:
        if word in used_words:
            continue
        used_words.add(word)

        if lives <= 0:
            break

        print(f'\nСлово №{len(used_words)} из {total_words}')
        guessed_letters = set()

        while True:
            print(display_word(word, guessed_letters))
            print(f'Количество жизней: {"♥" * lives}')
            if guessed_letters:
                print('Угадано:', ', '.join(sorted(guessed_letters)))

            guess = input("\nВведите букву или слово целиком: ").strip().lower()
            if not guess.isalpha():
                print(" Только буквы!")
                continue

            if len(guess) > 1:
                if guess == word.lower():
                    print(f'🎉 Верно! Слово — {word}')
                    score += 1
                    break
                else:
                    print(' Неверно!')
                    lives = 0
                    break

            if guess in guessed_letters:
                print(' Уже вводили эту букву.')
                continue

            guessed_letters.add(guess)

            if guess in word.lower():
                print(f'✅ Есть буква "{guess}"!')
                if all(letter.lower() in guessed_letters for letter in word):
                    print(f'🎉 Вы угадали слово: {word}')
                    score += 1
                    break
            else:
                lives -= 1
                print(f' Буквы "{guess}" нет. Осталось жизней: {lives}')
                if lives == 0:
                    break

        if lives == 0:
            print(f'\n💔 ИГРА ОКОНЧЕНА! 💔')
            print(f'Вы потратили все жизни! Загаданное слово было: {word}')
            break

        if score >= total_words:
            print('\n🎉 ПОЗДРАВЛЯЕМ! 🎉')
            print('Вы прошли всю игру и угадали все слова!')
            print('Вы настоящий ПОБЕДИТЕЛЬ игры "Поле чудес"! 🏆')
            print('\n🏆 ИДЕАЛЬНАЯ ИГРА! 🏆')
            break

    end_time = time.time()
    elapsed_time = int(end_time - start_time)
    minutes, seconds = divmod(elapsed_time, 60)

    print('\n=== ИГРА ЗАВЕРШЕНА ===')
    print('Спасибо за игру!')
    print('\n📊 Ваша статистика:')
    print(f'Угадано слов: {score} из {total_words}')
    print(f'Время игры: {minutes} мин {seconds} сек')

    high_scores = dict(get_high_scores())
    best_score = high_scores.get(player_name, 0)

    if score > best_score:
        print('🥇 Новый рекорд! Поздравляем!')
    else:
        print(f'Ваш лучший рекорд: {best_score} слов')

    update_record(player_name, score)


def WOFGame():
    print('=' * 50)
    print('Добро пожаловать в игру "ПОЛЕ ЧУДЕС"!')
    print('=' * 50)

    player = input('Введите ваше имя: ').strip() or "🤡🤡🤡"

    while True:
        play_game(player)

        again = input('\nХотите сыграть ещё раз? (д/н): ').strip().lower()
        if (again.lower())[0] != 'д':
            print('До новых встреч в игре "Поле чудес"!')
            break


def get_game_state(used_words):
    return {'used_words_count': len(used_words), 'player_name': "Текущий игрок"}
