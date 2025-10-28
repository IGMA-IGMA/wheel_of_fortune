import requests
from translatepy.translators.google import GoogleTranslate


gtranslate = GoogleTranslate()
url_random = "https://random-word-api.herokuapp.com/word"


def get_random_words(length: int = 10) -> list[str]:
    return [gtranslate.translate(
        requests.get(url=url_random).text[2:-2], "Russia"
    ).result.lower() + "\n"
        for _ in range(length)]
