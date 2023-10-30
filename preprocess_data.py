

### preprocess_data.py

def load_words_from_file(filename="all-possible-solutions.txt"):
    with open(filename, "r") as file:
        words = [line.strip() for line in file]
    return words

def create_word_scores(words):
    return {word: 1 for word in words}