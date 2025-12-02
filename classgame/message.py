class Message:
    """Класс для хранения всех текстовых сообщений игры 'Поле чудес'"""

    # Константы игры
    GAME_NAME = "ПОЛЕ ЧУДЕС"
    MAX_WORDS = 15
    HIDDEN_LETTER_SYMBOL = "■"
    LIFE_SYMBOL = "♥"

    # Эмодзи
    EMOJI: dict[str, int] = {
        "trophy": "🏆",
        "broken_heart": "💔",
        "confetti": "🎊",
        "celebration": "🎉",
    }

    LEVEL: dict[str, int] = {"1": 7, "2": 5, "3": 3}

    # Начало игры и меню
    @staticmethod
    def get_welcome_message(best_score: int) -> str:
        return f"=== {Message.GAME_NAME} ===\n{Message.EMOJI['trophy']} Ваш лучший рекорд: {best_score} слов"

    DIFFICULTY_PROMPT = "Выберите уровень сложности:"
    DIFFICULTY_OPTIONS = (
        "1. Легкий (7 жизней)\n2. Средний (5 жизней)\n3. Сложный (3 жизни)"
    )
    CHOICE_PROMPT = "Ваш выбор: "
    CHOISE_LEVEL_EX = "Не распознано!!!"

    # Ход игры
    @staticmethod
    def get_difficulty_level(choice: str) -> int:
        return Message.LEVEL[choice]

    @staticmethod
    def get_step_game(num_word, word_befor, life_user):
        return f"Слово №{num_word} из 15\n{word_befor}\nКоличество жизней: {"♥" * life_user}"

    @staticmethod
    def get_word_progress(current: int, total: int) -> str:
        return f"Слово №{current} из {total}"

    @staticmethod
    def get_lives_display(lives_count: int) -> str:
        return f"Количество жизней: {Message.LIFE_SYMBOL * lives_count}"

    GUESS_PROMPT = "Назовите букву или слово целиком: "

    @staticmethod
    def get_wrong_letter_message(letter: str) -> str:
        return f'Буквы "{letter}" нет в слове!'

    @staticmethod
    def get_word_guessed_message(word: str) -> str:
        return f"Слово отгадано: {word}\nВы выиграли! Приз в студию!"

    GAME_OVER_TITLE = f"💔 ИГРА ОКОНЧЕНА! 💔"

    @staticmethod
    def get_game_over_message(word: str) -> str:
        return f"К сожалению, у вас закончились жизни.\nЗагаданное слово было: {word.upper()}"

    CONGRATULATIONS_TITLE = f"🎉 ПОЗДРАВЛЯЕМ! 🎉"
    FULL_VICTORY_MESSAGE = "Вы прошли всю игру и угадали все 15 слов!"
    WINNER_MESSAGE = 'Вы настоящий ПОБЕДИТЕЛЬ игры "Поле чудес"!'
    PERFECT_GAME_TITLE = f"🏆 ИДЕАЛЬНАЯ ИГРА! 🏆"

    NEW_RECORD_TITLE = f"🎊 НОВЫЙ РЕКОРД! 🎊"
    NEW_RECORD_MESSAGE = "Вы установили новый личный рекорд!"

    @staticmethod
    def get_record_comparison(previous: int, current: int) -> str:
        return f"Предыдущий рекорд: {previous} слов\nНовый рекорд: {current} слов"

    STATS_TITLE = "📊 Ваш результат:"

    @staticmethod
    def get_words_guessed_stats(guessed: int, total: int) -> str:
        return f"Угадано слов: {guessed} из {total}"

    @staticmethod
    def get_play_time_stats(time: str) -> str:
        return f"Время игры: {time}"

    @staticmethod
    def get_best_score_stats(score: int) -> str:
        return f"Ваш лучший рекорд: {score} слов"

    @staticmethod
    def get_perfect_game_stats(time: str, level: str) -> str:
        return f"Общее время игры: {time}\nИспользованный уровень: {level}"

    RECORD_SAVED_MESSAGE = "Ваш результат записан в таблицу рекордов!"

    CONTINUE_PROMPT = "Хотите продолжить игру? (да/нет): "
    NEW_GAME_PROMPT = "Хотите начать новую игру? (да/нет): "

    SESSION_END_TITLE = "=== ИГРА ЗАВЕРШЕНА ==="
    THANK_YOU_MESSAGE = "Спасибо за игру!"
    FAREWELL_MESSAGE = 'До новых встреч в игре "Поле чудес"!'

    @staticmethod
    def get_game_over_full(
        word: str, guessed: int, total: int, time: str, best_score: int
    ) -> str:
        return (
            f"{Message.GAME_OVER_TITLE}\n"
            f"{Message.get_game_over_message(word)}\n\n"
            f"{Message.STATS_TITLE}\n"
            f"{Message.get_words_guessed_stats(guessed, total)}\n"
            f"{Message.get_play_time_stats(time)}\n"
            f"{Message.get_best_score_stats(best_score)}"
        )

    @staticmethod
    def get_new_record_full(
        previous: int, current: int, guessed: int, total: int, time: str
    ) -> str:
        return (
            f"{Message.NEW_RECORD_TITLE}\n"
            f"{Message.NEW_RECORD_MESSAGE}\n"
            f"{Message.get_record_comparison(previous, current)}\n\n"
            f"{Message.STATS_TITLE}\n"
            f"{Message.get_words_guessed_stats(guessed, total)}\n"
            f"{Message.get_play_time_stats(time)}"
        )

    @staticmethod
    def get_perfect_victory(time: str, level: str) -> str:
        return (
            f"{Message.CONGRATULATIONS_TITLE}\n"
            f"{Message.FULL_VICTORY_MESSAGE}\n"
            f"{Message.WINNER_MESSAGE}\n\n"
            f"{Message.PERFECT_GAME_TITLE}\n"
            f"{Message.get_perfect_game_stats(time, level)}\n"
            f"{Message.RECORD_SAVED_MESSAGE}"
        )

    @staticmethod
    def get_session_end_stats(
        guessed: int, total: int, time: str, best_score: int
    ) -> str:
        return (
            f"{Message.SESSION_END_TITLE}\n"
            f"{Message.THANK_YOU_MESSAGE}\n"
            f"{Message.STATS_TITLE}\n"
            f"{Message.get_words_guessed_stats(guessed, total)}\n"
            f"{Message.get_play_time_stats(time)}\n"
            f"{Message.get_best_score_stats(best_score)}\n\n"
            f"{Message.FAREWELL_MESSAGE}"
        )
