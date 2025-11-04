import linecache
import random
from typing import Optional

import randgen
from classgame.new_type import NewType


path_word_db = "data/words.txt"


def add_word_in_txt_file(
    path: NewType.file_path = path_word_db,
) -> Optional[bool] | Optional[Exception]:
    with open(file=path, mode="+a", encoding="utf-8") as file:
        file.writelines(randgen.get_random_words())
    file.close()
    return 1


def get_random_word_file(
    path: NewType.file_path = path_word_db,
) -> Optional[str] | Optional[Exception]:
    try:
        rand_word = linecache.getline(
            path, random.randint(1, len(open(path).readlines()))
        )
        return rand_word.rstrip()
    except Exception as ex:
        return ex


print(get_random_word_file())
