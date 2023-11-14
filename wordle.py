import requests
import json
import random
import preprocess_data
import tkinter as tk

# Create a tkinter window
root = tk.Tk()
root.geometry("500x500")
root.title("Wordle Game")

label = tk.Label(root, text="Wordle AI", font=('Times New Roman', 24))
label.pack(padx=20, pady=20)


# Create a frame to hold the black boxes
box_frame = tk.Frame(root)
box_frame.pack()

# Create 30 empty black boxes in a 5x6 pattern
white_boxes = []
for row in range(6):
    row_boxes = []
    for col in range(5):
        white_box = tk.Label(box_frame, width=6, height=3, bg="white", borderwidth=1, relief="solid")
        white_box.grid(row=row, column=col, padx=5, pady=5)
        row_boxes.append(white_box)
    white_boxes.append(row_boxes)



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

    target_char_count = {}  # Dictionary to store the count of each character in target_word
    for char in target_word:
        target_char_count[char] = target_char_count.get(char, 0) + 1

    #get greens first 
    for i in range(len(target_word)):
        if guessed_word[i] == target_word[i]:
            green_indexes.append(i)
            target_char_count[target_word[i]] -= 1

    #yellows and greys after greens
    for i in range(len(target_word)):
        if i not in green_indexes:
            if guessed_word[i] in target_word and target_char_count[guessed_word[i]] > 0:
                yellow_indexes.append(i)
                target_char_count[guessed_word[i]] -= 1
            else:
                white_indexes.append(i)

    return green_indexes, yellow_indexes, white_indexes

def filter_words(words, guess, green_indexes, yellow_indexes, white_indexes):

    new_filtered_words = []

    for word in words:
        #create simple lists of green and yellow letters
        green_letters = []
        for i in green_indexes:
            green_letters.append(guess[i])
        yellow_letters = []
        for j in yellow_indexes:
            yellow_letters.append(guess[j])

        #defualt keep word in filtered_list unless breaks a rule
        valid = True
        
        #dont keep words dont keep greens
        for index in green_indexes:
            if word[index] != guess[index]:
                valid = False
                break
        #dont keep yellows if dont move yellow spot or has yellow in it
        for index in yellow_indexes:
            if word[index] == guess[index] or guess[index] not in word:
                valid = False
                break
        #can eliminate grey in indexes where there isnt a green or yellow of that same letter
        for index in white_indexes:
            if guess[index] in green_letters and guess[index] not in yellow_letters:
                for idx in white_indexes:
                    if word[idx] == guess[index]:
                        valid = False
                        break
            elif guess[index] in yellow_letters:
                if word[index] == guess[index]:
                    valid = False
                    break
            elif guess[index] in word:
                valid = False
                break
        if valid:
            new_filtered_words.append(word)

    return new_filtered_words

word_list = preprocess_data.load_words_from_file()
filtered_words = word_list

# Main game loop
target_word = random.choice(word_list)
# target_word = "later"
guessed_words = []
url = 'https://wordle-api.vercel.app/api/wordle'
attempts = 0
max_attempts = 6


# Main game loop
start = False #can delete this later, using for testing purposes
while attempts < max_attempts:
    if start: #can delete later
        guess = "sally"
        start = False
    else:
        guess = random.choice(filtered_words)

    print(f"Attempt {attempts + 1}: Guess - '{guess}'")
    
    # Here, I am assuming the get_feedback function is replaced with the analyze_feedback
    green_indexes, yellow_indexes, white_indexes = analyze_feedback(target_word, guess)
    print(green_indexes, yellow_indexes)
    guessed_words.append(guess)

    #GUI code
    # print(attempts)
    i = 0
    while(i<5):
        white_boxes[attempts][i].config(text=guess[i])
        if i in green_indexes:
            white_boxes[attempts][i].config(bg="#4CAF50")
        elif i in yellow_indexes:
            white_boxes[attempts][i].config(bg="#FFC107")
        else:
            white_boxes[attempts][i].config(bg="#808080")
        i+=1

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
root.mainloop()
