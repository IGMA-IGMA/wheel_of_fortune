import json
import random
from typing import List, Iterator

from wheel_of_fortune.utils import FilePath, IterWord
from wheel_of_fortune.logging_utils import log_errors

PATH_WORDS_JSON: FilePath = "data/rusword.json"
PATH_GAME_WORDS: FilePath = "data/words.txt"
PATH_RECORD: FilePath = "data/record.txt"

@log_errors
def prepare_words(count: int = 15) -> None:
    with open(PATH_WORDS_JSON, "r", encoding="utf-8") as f:
        words: List[str] = json.load(f)
    selected = random.sample(words, count) if len(words) >= count else words.copy()
    with open(PATH_GAME_WORDS, "w", encoding="utf-8") as f:
        f.write("\n".join(selected))

@log_errors
def word_generator() -> Iterator[str]:
    with open(PATH_GAME_WORDS, "r", encoding="utf-8") as f:
        for line in f:
            yield line.strip()

@log_errors
def load_record() -> int:
    try:
        with open(PATH_RECORD, "r", encoding="utf-8") as f:
            s = f.read().strip()
            return int(s)
    except (FileNotFoundError, ValueError):
        return 0

@log_errors
def save_record(new_record: int) -> None:
    with open(PATH_RECORD, "w", encoding="utf-8") as f:
        f.write(str(new_record))
