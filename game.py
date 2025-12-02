from typing import Tuple

from classgame import message as m
from classgame import user_info
from classgame.new_type import NewType
from file_handler import out_word
from work_with_word import replace_letter, start_word_ind

message = m.Message()
user = user_info.User()

# status_game


def game_one_word(life_user, word, num_word):

    cout = start_word_ind(word)
    word_befor, letter_check = cout["result"]

    while word_befor != word and life_user:
        print(message.get_step_game(num_word, word_befor, life_user))

        user_input = input(message.GUESS_PROMPT)
        if len(user_input) > 1:
            return user_input == word
        if user_input in letter_check:
            cin = replace_letter(user_input, word_befor, letter_check)
            _, word_befor = cin["exception"], cin["result"]
        else:
            print(message.get_wrong_letter_message(user_input))
            life_user -= 1
    return bool(life_user)


def game_init() -> Tuple[NewType.iter_word, int]:
    print(message.get_welcome_message(user.word_max))

    print(message.DIFFICULTY_PROMPT, message.DIFFICULTY_OPTIONS, sep="\n")

    cin = input(message.CHOICE_PROMPT)
    difficulty_level = message.get_difficulty_level(cin)

    return out_word(), difficulty_level


def game_guess_cycle():
    slovar_gen, life_user = game_init()
    counter_gen = 1
    while counter_gen != 16:
        word = next(slovar_gen)
        flag_one_word = game_one_word(
            life_user=life_user, word=word, num_word=counter_gen
        )
        if flag_one_word:
            counter_gen += 1
            user.word_now += 1
            print(message.get_word_guessed_message(word))
        else:
            
            print(message.get_game_over_message(word))