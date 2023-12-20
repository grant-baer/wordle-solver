# wordle-solver

**Wordle Solver**

Overview
This program is an intelligent engine designed to solve the popular word puzzle game, Wordle. The aim is to guess the correct five-letter word within the least number of attempts.

How It Works
Initial Guess: The engine starts with a wide library of five-letter words.
Feedback Analysis: After each guess, the game's feedback is used to prune the word library, eliminating words that no longer fit the given clues.
Next Guesses: Using a refined list, the engine makes subsequent guesses that are more informed and targeted.
Solution Path: The decision tree within the program visualizes the process of narrowing down the word library until the correct word is found.

Features
Efficient Algorithm: Designed to reach the correct answer in the fewest guesses possible.
Feedback Integration: Dynamically updates the possible answers based on the game's colored tile feedback.
GUI of Decision Process: Provides a clear representation of the guessing process and the next choice of words.
