class Message:
    GAME_NAME = "ПОЛЕ ЧУДЕС"
    LIFE_SYMBOL = "♥"

    @staticmethod
    def welcome(best_score: int) -> str:
        return f"=== {Message.GAME_NAME} ===\n🏆 Ваш лучший рекорд: {best_score} слов"

    @staticmethod
    def choose_difficulty_prompt() -> str:
        return ("Выберите уровень сложности:\n"
                "1 — Легкий (7 жизней)\n"
                "2 — Средний (5 жизней)\n"
                "3 — Сложный (3 жизни)\n"
                "Ваш выбор: ")

    @staticmethod
    def invalid_choice() -> str:
        return "Неверный выбор, попробуйте ещё раз."

    @staticmethod
    def word_state(word_masked: str, lives: int) -> str:
        return f"{word_masked}\nЖизней: {Message.LIFE_SYMBOL * lives}"

    @staticmethod
    def guess_prompt() -> str:
        return "Назовите букву или слово целиком: "

    @staticmethod
    def wrong_letter(letter: str) -> str:
        return f'Буквы "{letter}" нет в слове!'

    @staticmethod
    def wrong_word(word: str) -> str:
        return f'Слово "{word}" неверное!'

    @staticmethod
    def word_guessed(word: str) -> str:
        return f"Слово отгадано: {word}"

    @staticmethod
    def game_over(word: str) -> str:
        return (f"💔 ИГРА ОКОНЧЕНА! 💔\n"
                f"К сожалению, у вас закончились жизни.\n"
                f"Загаданное слово: {word}")

    @staticmethod
    def victory() -> str:
        return "🎉 ПОЗДРАВляю! Вы угадали все слова!"

    @staticmethod
    def new_record(old: int, new: int) -> str:
        return (f"🎊 НОВЫЙ РЕКОРД! 🎊\n"
                f"Предыдущий рекорд: {old} слов\n"
                f"Новый рекорд: {new} слов")

    @staticmethod
    def goodbye(guessed: int, total: int, best: int) -> str:
        return ("Спасибо за игру!\n"
                f"Угадано слов: {guessed} из {total}\n"
                f"Ваш лучший рекорд: {best} слов")
