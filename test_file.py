from translatepy.translators.google import GoogleTranslate
import json


gtranslate = GoogleTranslate()

with open("data/engword.json", "r", encoding="utf-8") as fileng:
    dataeng = json.load(fileng)
fileng.close()


datarus = []
for word in dataeng:

    wordrus = gtranslate.translate(word, "Russia").result
    if wordrus.count(" "):
        continue
    datarus += [datarus]

with open("data/rusword.json", "w", encoding="utf-8") as filerus:
    json.dump(datarus, filerus, ensure_ascii=False, indent=4)
