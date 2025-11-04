class User:
    def __init__(
        self, word_max: int = 0, word_now: int = 0, time_game: list[int] = [0, 0]
    ):
        self.word_max = word_max
        self.word_now = word_now
        # минуты секунды
        self.time_game = time_game
