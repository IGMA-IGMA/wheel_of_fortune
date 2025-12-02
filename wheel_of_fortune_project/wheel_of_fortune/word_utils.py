from typing import Tuple
from wheel_of_fortune.utils import LetterPositions
from wheel_of_fortune.logging_utils import log_errors

@log_errors
def mask_word(word: str, mask_char: str = "■") -> Tuple[str, LetterPositions]:
    letter_positions: LetterPositions = {}
    masked_chars = []
    for idx, ch in enumerate(word):
        if ch in (" ", "-"):
            masked_chars.append(ch)
        else:
            masked_chars.append(mask_char)
            letter_positions.setdefault(ch, []).append(idx)
    return "".join(masked_chars), letter_positions

@log_errors
def reveal_letter(masked: str, letter: str, positions: LetterPositions) -> str:
    chars = list(masked)
    for pos in positions.get(letter, []):
        chars[pos] = letter
    return "".join(chars)
