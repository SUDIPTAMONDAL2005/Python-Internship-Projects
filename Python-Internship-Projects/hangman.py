"""Task 1: Hangman Word Guessing Game (Console)."""
import random

WORDS = ["python", "developer", "internship", "keyboard", "function",
         "variable", "program", "computer", "github", "terminal"]
MAX_ATTEMPTS = 6

# One ASCII picture for each number of wrong guesses (0 to 6).
STAGES = [
    """
  +---+
  |   |
      |
      |
      |
      |
=========""",
    """
  +---+
  |   |
  O   |
      |
      |
      |
=========""",
    """
  +---+
  |   |
  O   |
  |   |
      |
      |
=========""",
    """
  +---+
  |   |
  O   |
 /|   |
      |
      |
=========""",
    """
  +---+
  |   |
  O   |
 /|\\  |
      |
      |
=========""",
    """
  +---+
  |   |
  O   |
 /|\\  |
 /    |
      |
=========""",
    """
  +---+
  |   |
  O   |
 /|\\  |
 / \\  |
      |
=========""",
]


def play_round():
    word = random.choice(WORDS)
    correct = set()   # right letters
    wrong = set()     # wrong letters

    print("\n" + "=" * 34)
    print("   HANGMAN WORD GUESSING GAME")
    print("=" * 34)

    while True:
        mistakes = len(wrong)
        print(STAGES[mistakes])
        print("\nWord:", " ".join(l if l in correct else "_" for l in word))
        print("Guessed letters:", ", ".join(sorted(correct | wrong)) or "none")
        print(f"Attempts left: {MAX_ATTEMPTS - mistakes}")

        if all(letter in correct for letter in word):
            print(f"\nYou won! The word was '{word}'.")
            return
        if mistakes >= MAX_ATTEMPTS:
            print(f"\nGame over! The word was '{word}'.")
            return

        guess = input("\nEnter one letter: ").strip().lower()

        if len(guess) != 1 or not guess.isalpha():
            print("Please enter a single letter (a-z).")
        elif guess in correct or guess in wrong:
            print(f"You already guessed '{guess}'. No attempt lost.")
        elif guess in word:
            correct.add(guess)
            print("Good guess!")
        else:
            wrong.add(guess)
            print("Wrong guess!")


def main():
    while True:
        play_round()
        again = input("\nPlay again? (yes/no): ").strip().lower()
        if again not in ("yes", "y"):
            print("Thanks for playing!")
            break


if __name__ == "__main__":
    main()
