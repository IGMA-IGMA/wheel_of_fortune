import json
import linecache
import random
from typing import Optional

from classgame.new_type import NewType

from decorators import handle_result

path_word_game_db: NewType.file_path = "data/words.txt"
path_word_db: NewType.file_path = "data/rusword.json"


@handle_result
def load_random_words_optimized(
    count: int = 15
) -> None:
    with open(path_word_db, 'r', encoding='utf-8') as f:
        words = json.load(f)

    if len(words) > 10000:
        selected = words[:count]
        for i in range(count, len(words)):
            j = random.randint(0, i)
            if j < count:
                selected[j] = words[i]
        selected_words = selected
    else:
        selected_words = random.sample(words, min(count, len(words)))

    with open(path_word_game_db, 'w', encoding='utf-8') as f:
        f.write('\n'.join(selected_words))


def out_word():
    for word in open(path_word_game_db, encoding='utf-8'):
        yield word.rstrip()
