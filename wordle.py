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

# Function to get the feedback for a guess
def get_feedback(target_word, guess):
    correct_characters = sum([1 for a, b in zip(target_word, guess) if a == b])
    correct_positions = sum([1 for a, b in zip(target_word, guess) if a == b])
    return correct_characters, correct_positions

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


word_list = preprocess_data.load_words_from_file()

# Main game loop
target_word = random.choice(word_list)
guessed_words = []
url = 'https://wordle-api.vercel.app/api/wordle'
attempts = 0
max_attempts = 20

while attempts < max_attempts:
    print(f"\nAttempt {attempts + 1}/{max_attempts}")
    print(f"Target Word: {target_word}")
    
    # Choose the next guess based on the narrowed word list, excluding already guessed words
    possible_words = [word for word in word_list if word not in guessed_words]
    if possible_words:
        if attempts == 0:  # First guess
            guess = random.choice(possible_words)
        else:
            # Determine green and yellow indexes of the previous word
            green_indexes, yellow_indexes, _ = analyze_feedback(target_word, guessed_words[-1])
            next_guess = None

            for word in possible_words:
                # Check if the green indexes of the previous word match the current word
                if all(word[i] == target_word[i] for i in green_indexes):
                    # Check if the yellow indexes are in new positions
                    if all(word[i] != target_word[i] for i in yellow_indexes):
                        next_guess = word
                        break
            
            if next_guess:
                guess = next_guess
            else:
                # If no suitable word is found, choose a random word
                guess = random.choice(possible_words)
    else:
        print("No more unguessed words in the list. You may have made an incorrect guess.")
        break
    
    print(f"Guess: {guess}")
    
    correct_characters, correct_positions = get_feedback(target_word, guess)
    print(f"Correct Characters: {correct_characters}")
    print(f"Correct Positions: {correct_positions}")
    
    if correct_characters == len(target_word) and correct_positions == len(target_word):
        print(f"Congratulations! You've guessed the word: {target_word}")
        break

    guessed_words.append(guess)
    word_list = [word for word in word_list if get_feedback(target_word, word) == (correct_characters, correct_positions)]
    
    if not word_list:
        print("No more words in the list match the feedback. You may have made an incorrect guess.")
        break

    attempts += 1

if attempts == max_attempts:
    print(f"Sorry, you've reached the maximum number of attempts. The word was: {target_word}")
