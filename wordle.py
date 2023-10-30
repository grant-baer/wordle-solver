import requests
import json

def display_wordle_result(data, guess):
    print(f"Guess: {guess}")
    print(f"Was Correct: {data['was_correct']}")
    for info in data['character_info']:
        char = info['char']
        in_word = info['scoring']['in_word']
        correct_idx = info['scoring']['correct_idx']
        print(f"Character: {char}, In Word: {in_word}, Correct Index: {correct_idx}")
    print("\n")

url = 'https://wordle-api.vercel.app/api/wordle'
attempts = 0
max_attempts = 6

while attempts < max_attempts:
    guess = input(f"Enter guess {attempts + 1}/{max_attempts}: ")
    
    myobj = {
        "guess": guess
    }

    response = requests.post(url, json=myobj)

    if response.status_code == 200:
        data = json.loads(response.text)
        display_wordle_result(data, guess)

        if data['was_correct']:
            print("You've guessed the word! Congrats!")
            break
        else:
            attempts += 1
    else:
        print("Failed to make the API request. Status code:", response.status_code)
        break

if attempts == max_attempts:
    print(f"Sorry, you've reached the maximum number of attempts. The word was not guessed.")
