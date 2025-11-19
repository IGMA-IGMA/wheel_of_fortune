from codecs import replace_errors
from typing import Tuple

from classgame import message as m
from classgame import user_info
from classgame.new_type import NewType
from file_handler import out_word
from work_with_word import start_word_ind, replace_letter

message = m.Message()
user = user_info.User()

# status_game


def game_one_word(life_user, word, num_word):
    print(message.)
    cout = start_word_ind(word)
    word_befor, letter_check = cout["result"]
    print(message.get_step_game(num_word, word_befor, life_user))

    
    while word_befor != word or life_user:
        user_input = input(message.GUESS_PROMPT)
        if len(user_input) > 1:
            if user_input == word:
                return 1
            else:
                return 0
        if user_input in letter_check:
            _, word_befor = replace_letter()
            print(message.)
        else:
            life_user -= 1


def game_init() -> Tuple[NewType.iter_word, int]:
    print(message.get_welcome_message(user.word_max))

    print(message.DIFFICULTY_PROMPT, message.DIFFICULTY_OPTIONS, sep="\n")

    cin = input()
    difficulty_level = message.get_difficulty_level(cin)

    return out_word(), difficulty_level


def game_guess_cycle():
    slovar_gen, life_user = game_init()
    conter_gem = 1
    while life_user and conter_gem != 15:
        word = next(slovar_gen)

    if not life_user:
        print(
            message.GAME_OVER_TITLE,
        )


if __name__ == "__main__":
    print(game_one_word(1, "fghjk"))
