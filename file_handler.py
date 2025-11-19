import json
import random
from typing import Any, Generator

from classgame.new_type import NewType
from classgame.user_info import User
from decorators import handle_result

path_word_game_db: NewType.file_path = "data/words.txt"
path_word_db: NewType.file_path = "data/rusword.json"
path_rec_user: NewType.file_path = "data/record.txt"


@handle_result
def load_random_words_optimized(count: int = 15) -> None:
    with open(path_word_db, "r", encoding="utf-8") as f:
        words = json.load(f)

    if len(words) > 10000:
        selected = words[:count]
        for i in range(count, len(words)):
            j: int = random.randint(0, i)
            if j < count:
                selected[j] = words[i]
        selected_words = selected
    else:
        selected_words: list[Any] = random.sample(words, min(count, len(words)))

    with open(path_word_game_db, "w", encoding="utf-8") as f:
        f.write("\n".join(selected_words))


@handle_result
def load_result_file(user: User) -> None:
    with open(path_rec_user, "w") as file:
        file.write(user.word_max)
    file.close()


def out_word() -> Generator[str, Any, None]:
    for word in open(path_word_game_db, encoding="utf-8"):
        yield word.rstrip()
