import randgen
import linecache
import random
from typing import Optional

path_word_db = "data/words.txt"
Path = "data\\words.txt"


def add_word_in_txt_file(path: Optional[str] = path_word_db) -> Optional[bool] | Optional[Exception]:
    try:
        with open(file=path, mode="+a", encoding="utf-8") as file:
            file.writelines(randgen.get_random_words())
        file.close()
        return 1
    except Exception as ex:
        return ex


def get_random_word_file(path: Optional[str] = Path) -> Optional[str] | Optional[Exception]:
    try:
        rand_word = linecache.getline(
            path, random.randint(1, len(open(path).readlines())))
        return rand_word.rstrip()
    except Exception as ex:
        return ex