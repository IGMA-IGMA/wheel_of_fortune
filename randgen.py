from typing import List, Optional

import requests
from translatepy.translators.google import GoogleTranslate

gtranslate = GoogleTranslate()
Url_random = "https://random-word-api.herokuapp.com/word"
Path = "data\\words.txt"


def get_random_words(length: Optional[int] = 15) -> List[str]:
    data_words = []
    while len(data_words) < length:
        print(data_words)
        word = gtranslate.translate(
            requests.get(url=Url_random).text[2:-2], "Russia"
        ).result.lower()
        if word.count(" "):
            continue
        data_words += [word + "\n"]
    return data_words
