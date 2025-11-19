from typing import Optional

from classgame.new_type import NewType
from decorators import handle_result


@handle_result
def start_word_ind(word: Optional[str]) -> NewType.ret_dict:
    letter_otvet = {}
    for i in range(len(word)):
        if word[i] in "- ":
            continue
        elif word[i] not in letter_otvet:
            letter_otvet[word[i]] = [i]
        else:
            letter_otvet[word[i]] += [i]
    return ["".join(["■" if i != "-" else "-" for i in word]), letter_otvet]


@handle_result
def replace_letter(
    letter: str, word_square: str, letter_dict: NewType.letter_dict
) -> NewType.ret_dict:
    word_square = list(word_square)
    for i in letter_dict[letter]:
        word_square[i] = letter
    return "".join(word_square)
