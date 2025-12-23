def display_word(word, guessed_letters):
    word_to_guess = []
    for letter in word:
        if letter.lower() in guessed_letters:
            word_to_guess.append(letter)
        else:
            word_to_guess.append('■')
    return ' '.join(word_to_guess)