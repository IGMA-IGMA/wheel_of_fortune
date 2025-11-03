from typing import Optional
from classgame.new_type import NewType


def start_word_ind(word: Optional[str]) -> NewType.letter_dict:
    letter_otvet = {}
    for i in range(len(word)):
        if word[i] == '-':
            continue
        elif word[i] not in letter_otvet:
            letter_otvet[word[i]] = [i]
        else:
            letter_otvet[word[i]] += [i]
    return letter_otvet


def start_square(word: Optional[str]) -> Optional[str]:
    return "".join(["■" if i != '-' else '-' for i in word])


def replace_letter():
    pass


print(start_square("w-o-r-d"))
