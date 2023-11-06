import requests
import json
import random
import preprocess_data

def display_wordle_result(data, guess):
    print(f"Guess: {guess}")
    print(f"Was Correct: {data['was_correct']}")
    for info in data['character_info']:
        char = info['char']
        in_word = info['scoring']['in_word']
        correct_idx = info['scoring']['correct_idx']
        print(f"Character: {char}, In Word: {in_word}, Correct Index: {correct_idx}")
    print("\n")

def analyze_feedback(target_word, guessed_word):
    green_indexes = []  # Correct character in correct position
    yellow_indexes = []  # Correct character in incorrect position
    white_indexes = []  # Incorrect character

    for i in range(len(target_word)):
        if guessed_word[i] == target_word[i]:
            green_indexes.append(i)
        elif guessed_word[i] in target_word:
            yellow_indexes.append(i)
        else:
            white_indexes.append(i)

    return green_indexes, yellow_indexes, white_indexes

def filter_words(words, guess, green_indexes, yellow_indexes, white_indexes):
    new_filtered_words = []
    for word in words:
        valid = True
        for index in green_indexes:
            if word[index] != guess[index]:
                valid = False
                break
        for index in yellow_indexes:
            if word[index] == guess[index] or guess[index] not in word:
                valid = False
                break
        for index in white_indexes:
            if guess[index] in word:
                valid = False
                break
        if valid:
            new_filtered_words.append(word)
    return new_filtered_words

word_list = preprocess_data.load_words_from_file()
filtered_words = word_list

# Main game loop
target_word = random.choice(word_list)
guessed_words = []
url = 'https://wordle-api.vercel.app/api/wordle'
attempts = 0
max_attempts = 6


# Main game loop
while attempts < max_attempts:
    guess = random.choice(filtered_words)
    print(f"Attempt {attempts + 1}: Guess - '{guess}'")
    
    # Here, I am assuming the get_feedback function is replaced with the analyze_feedback
    green_indexes, yellow_indexes, white_indexes = analyze_feedback(target_word, guess)
    print(green_indexes, yellow_indexes)
    guessed_words.append(guess)

    # Check if the guess is correct
    if len(green_indexes) == len(target_word):
        print(f"Correct! The word is '{guess}'.")
        break
    
    # Filter the list of words based on the feedback
    filtered_words = filter_words(filtered_words, guess, green_indexes, yellow_indexes, white_indexes)
    attempts += 1

    # If there are no more words left, the game is over
    if not filtered_words:
        print("No more possible words left to guess.")
        break


# After the loop
if target_word == guessed_words[-1]:
    print(f"Wordle solved in {attempts+1} attempts!")
else:
    print(f"Failed to solve Wordle. The word was '{target_word}'.")



#Attempt 3: Guess - 'naras'
#[0, 1, 4] [3]
#The word was 'naffs'.

# if two 'e' letters give feedback yellow and target only has one 'e'
# only give the first letter 'e' as yellow
# green takes priority for any colored letter (example shown above)


