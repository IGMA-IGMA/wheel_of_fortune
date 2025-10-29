import gener

path_word_db = "data/words.txt"


def add_word_in_txt_file(path: str = path_word_db) -> bool | Exception:
    try:
        with open(file=path, mode="+a", encoding="utf-8") as file:
            file.writelines(gener.get_random_words())
        file.close()
        return 1
    except Exception as ex:
        return ex


