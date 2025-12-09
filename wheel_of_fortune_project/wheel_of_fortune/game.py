from wheel_of_fortune.file_handler import prepare_words, word_generator, load_record, save_record
from wheel_of_fortune.word_utils import mask_word, reveal_letter
from wheel_of_fortune.messages import Message


def choose_lives() -> int:
    while True:
        choice = input(Message.choose_difficulty_prompt()).strip()
        if choice == "1":
            return 7
        elif choice == "2":
            return 5
        elif choice == "3":
            return 3
        else:
            print(Message.invalid_choice())


def play_one_word(word: str) -> bool:
    masked, positions = mask_word(word)
    lives = choose_lives()

    while lives > 0 and masked != word:
        print(Message.word_state(masked, lives))
        user_input = input(Message.guess_prompt()).strip().lower()

        if not user_input:
            continue

        # ───────────────────────────────────────────────
        # Если введено больше одной буквы → это попытка угадать слово
        # ───────────────────────────────────────────────
        if len(user_input) > 1:
            if user_input == word:
                print(Message.word_guessed(word))
                return True
            else:
                print(Message.wrong_word(user_input))
                return False  # сразу проигрыш
        else:
            # Обычная попытка — буква
            letter = user_input
            if letter in positions and letter not in masked:
                masked = reveal_letter(masked, letter, positions)
            else:
                lives -= 1
                print(Message.wrong_letter(letter))

    if masked == word:
        print(Message.word_guessed(word))
        return True
    else:
        return False


def game_loop():
    best = load_record()
    print(Message.welcome(best))

    prepare_words()
    words = word_generator()

    total = 0
    guessed = 0

    for word in words:
        total += 1
        print(f"\nСлово №{total}\n")
        success = play_one_word(word)
        if success:
            guessed += 1
        else:
            print(Message.game_over(word))
            break
    else:
        print(Message.victory())

    print("\nРезультат:")
    print(f"Угадано {guessed} из {total}")

    if guessed > best:
        save_record(guessed)
        print(Message.new_record(best, guessed))

    print(Message.goodbye(guessed, total, max(best, guessed)))


def main():
    while True:
        game_loop()
        again = input("\nХотите сыграть ещё раз? (y/n): ").strip().lower()
        if again != "y":
            print("Спасибо за игру! До встречи!")
            break


if __name__ == "__main__":
    main()
