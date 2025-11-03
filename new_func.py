from typing import Optional
from classgame import new_type

type letter_dict = dict[str, list[int]]

def start_word_ind(word: Optional[str]) -> dict[str, list[int]]:
    letter_otvet = {}
    for i in range(len(word)):
        if word[i] not in l:
             = []


def start_square(word: Optional[str]) -> Optional[str]:
    return len(word) * "■"


def replace_letter()
