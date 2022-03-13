def WordleBot(name):
    word_list = extract_word_list()
    Introductions()
    solve_wordle(word_list)


def Introductions():
    print('Hello! Thanks for checking out my WordleBot!'
          '\nTo enter a guess, put each letter followed by \'0\', \'1\', or \'3\' and a space:'
          '\n\'0\': The letter is grey, and is not contained in the word.'
          '\n\'1\': The letter is yellow, and is in the word in a different spot.'
          '\n\'3\': The letter is green, and is in the word in that spot.'
          '\nHere\'s an example input: \'h0 eY l0 l0 oG\''
          '\nIn this case, \'e\' is in the word, and \'o\' is the last letter.'
          '\nAfter every guess, the WordleBot will provide you with a list of words that could be the solution.'
          '\nThe WordleBot will automatically place the most common words at the beginning of the list.'
          '\nGood luck, Have fun!')


def extract_word_list():
    with open('5_letter_words.txt') as words:
        word_string = words.read()
        word_list = word_string.splitlines()
    return word_list


def solve_wordle(word_list):
    viable_words = list(word_list)
    the_word = {}  # Format: [index : [is, [is not]]]
    for x in range(0, 5):
        the_word[x] = ['', []]
    word_contains = []
    word_does_not_contain = []
    while len(viable_words) > 1:
        guess = input('Enter your guess: ')
        guess_list = list(guess.replace(' ', ''))
        for x in range(0, 9):
            if x % 2 == 0:
                index = int(x / 2)
                if guess_list[x + 1] == '0':
                    for num in range(0, 5):
                        the_word[num][1].append(guess_list[x])
                        word_does_not_contain.append(guess_list[x])
                if guess_list[x + 1] == '1':
                    word_contains.append(guess_list[x])
                    the_word[index][1].append(guess_list[x])
                if guess_list[x + 1] == '3':
                    the_word[index][0] = guess_list[x]
        print(f'Number of possible solutions before input: {len(viable_words)}')
        for word in word_list:
            # Check we have all known yellow letters
            contains_all_yellow_letters = True
            word_to_list = list(word)
            for letter in word_contains:
                if letter not in word_to_list:
                    contains_all_yellow_letters = False
            if not contains_all_yellow_letters and word in viable_words:
                viable_words.remove(word)

            for index in range(0, 5):
                # Any words with yellow letters in the same spot are not viable
                for yellow_letter in the_word[index][1]:
                    if yellow_letter in word and word.index(yellow_letter) == index and word in viable_words:
                        viable_words.remove(word)
                # If we have green letters, make sure the word has them and that they're in the right spot.
                if not the_word[index][0] == '' and the_word[index][0] not in word and word in viable_words:
                    viable_words.remove(word)
                if not the_word[index][0] == '' and the_word[index][0] in word and word in viable_words:
                    if not index == word.index(the_word[index][0]) and word in viable_words:
                        viable_words.remove(word)

                # Check we don't have any uncontained letters
                if the_word[index][1] is not None:
                    for uncontained_letter in word_does_not_contain:
                        if uncontained_letter in word and word in viable_words:
                            viable_words.remove(word)
        print(f'Number of possible solutions after input: {len(viable_words)}')
        print(f'Remaining possible solutions: {viable_words}')


if __name__ == '__main__':
    WordleBot()
