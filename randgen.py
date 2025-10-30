import requests
from translatepy.translators.google import GoogleTranslate
import linecache
import random


gtranslate = GoogleTranslate()
Url_random = "https://random-word-api.herokuapp.com/word"
Path = "data\\words.txt"



def get_random_words(length: int = 10) -> list[str]:
    data_words = []
    while len(data_words) < length:
        word = requests.get(url=Url_random).text[2:-2]
    return [gtranslate.translate(
        requests.get(url=Url_random).text[2:-2], "Russia"
    ).result.lower() + "\n"
        for _ in range(length)]


def get_random_word_file(path: str = Path) -> str | Exception:
    rand_word = linecache.getline(
        path, random.randint(1, len(open(path).readlines())))
    return rand_word.rstrip()


