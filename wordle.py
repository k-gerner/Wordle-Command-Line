try:
    from curses import wrapper
except ImportError:
    print("""
    This program uses the Python curses module for cleaner command line printing.
    Unfortunately, this is not available on Windows operating systems.
    Please instead use v1.1.0, which is the latest available version of the program
    that does not use the curses module:
    https://github.com/k-gerner/Wordle-Command-Line/releases/tag/v1.1.0
    """)
    quit()

import os
import sys
import random
from typing import Tuple
from collections import defaultdict
from printutil import PrintMode
from wordle_printer import WordlePrinter
from board import *

VALID_GUESSES = set()  # all 5 letter words
POSSIBLE_ANSWERS = []  # all words that could still be valid guesses according to previous letter scores

HISTORY_FILE = 'history.txt'


def build_word_collections(guesses_filename: str, answers_filename: str) -> None:
    """Populates the VALID_GUESSES and POSSIBLE_ANSWERS collections"""
    global VALID_GUESSES, POSSIBLE_ANSWERS
    with open(guesses_filename, 'r') as guesses_file:
        for word in guesses_file:
            VALID_GUESSES.add(word.strip().lower())
    with open(answers_filename, 'r') as answers_file:
        for word in answers_file:
            POSSIBLE_ANSWERS.append(word.strip().lower())


def evaluate_guess(guess_str: str, answer: str) -> Guess:
    """
    Evaluates the guess and returns a Guess object, which contains (in part)
    a list of scores corresponding to each letter.
    """
    # first check for all the correctly guessed letters
    # This must be done before checking for wrong spot / incorrect letters
    guess_obj = Guess(guess_str)
    for i, guessed_char in enumerate(guess_str):
        if guessed_char == answer[i]:
            guess_obj.set_score(i, CORRECT)
            answer = answer[:i] + "_" + answer[i + 1:]
        else:
            guess_obj.set_score(i, INCORRECT)
    for i in guess_obj.get_inaccurate_indices():
        if guess_str[i] in answer:
            guess_obj.set_score(i, WRONG_SPOT)
            true_location = answer.index(guess_str[i])
            answer = answer[:true_location] + "_" + answer[true_location + 1:]
    return guess_obj


def is_valid_hard_mode_guess(board, word, answer) -> bool:
    """Checks if the word is a valid guess in hard mode"""
    guess_obj = evaluate_guess(word, answer)
    if guess_obj.is_correct():
        return True
    previous_guess_obj = board.most_recent_guess()
    previous_guess_str = previous_guess_obj.word
    new_letters_to_num_found = defaultdict(int)   # [letter, count]
    prev_yellow_letters_counts = defaultdict(int)  # [letter, count]
    for index, prev_letter_score in enumerate(previous_guess_obj.scores):
        new_score_at_index = guess_obj.scores[index]
        if prev_letter_score == CORRECT:
            if new_score_at_index != CORRECT:
                return False
            else:
                # if both correct, don't add to dicts
                continue
        elif prev_letter_score == WRONG_SPOT:
            prev_yellow_letters_counts[previous_guess_str[index]] += 1

        if new_score_at_index in [CORRECT, WRONG_SPOT]:
            new_letters_to_num_found[word[index]] += 1

    for prev_letter, num_yellow in prev_yellow_letters_counts.items():
        if new_letters_to_num_found[prev_letter] < num_yellow:
            return False
    return True


def get_user_guess(board, printer, hard_mode, answer) -> str:
    """Gets the guess word from the user"""
    guess = printer.get_input("Type your guess (or 'q' to quit):\t").strip().lower()
    while True:
        if guess == 'q':
            quit()
        elif guess == "" or len(guess) != 5:
            guess = printer.get_input("Must be 5 letters. Try again:  ", print_mode=PrintMode.ERROR).strip().lower()
        elif board.guessed_already(guess):
            guess = printer.get_input("You've already guessed that word. Try again:  ", print_mode=PrintMode.ERROR).strip().lower()
        elif not guess.isalpha():
            guess = printer.get_input("Must only contain letters. Try again:  ", print_mode=PrintMode.ERROR).strip().lower()
        elif guess not in VALID_GUESSES:
            guess = printer.get_input("Not a valid word. Try again:  ", print_mode=PrintMode.ERROR).strip().lower()
        elif hard_mode and board.num_guesses() >= 1 and not is_valid_hard_mode_guess(board, guess, answer):
            text = "Since you're in hard mode, you must use all letters found already. Try again:\t"
            guess = printer.get_input(text, print_mode=PrintMode.ERROR).strip().lower()
        else:
            break
    return guess


def tally_game(win: bool) -> Tuple[int, int]:
    """
    Adds to the game history file to keep track of total wins across all runs
    Returns a tuple: (# wins, total games)
    """
    num_wins = 1 if win else 0
    total_games = 1
    if os.path.isfile(HISTORY_FILE):
        with open(HISTORY_FILE, 'r') as file:
            num_wins += int(file.readline().strip())
            total_games += int(file.readline().strip())
    with open(HISTORY_FILE, 'w') as file:
        file.write(str(num_wins) + '\n')
        file.write(str(total_games) + '\n')
        file.write(
            "# Do not modify. This file keeps track of the total # of wins and games you have played.\n")
        file.write("# If you delete this file, your past games history will be reset.")
    return num_wins, total_games


def play_game(board, printer, hard_mode, previous_answers, answer=None) -> None:
    """Play the game from start to finish"""
    if not answer:
        answer = random.choice(POSSIBLE_ANSWERS).lower()
        while answer in previous_answers:
            answer = random.choice(POSSIBLE_ANSWERS).lower()
        previous_answers.append(answer)
    game_won = False
    printer.show_all_windows(board)
    for turn in range(6):
        printer.show_all_windows(board)
        guess_str = get_user_guess(board, printer, hard_mode, answer)
        guess_obj = evaluate_guess(guess_str, answer)
        board.add_guess(guess_obj)
        printer.update_board(board)
        if guess_obj.is_correct():
            game_won = True
            break
    num_wins, num_games = tally_game(game_won)
    if game_won:
        printer.show_win_message(board)
    else:
        printer.show_loss_message()
        replay = printer.get_input("Would you like to replay with the same word? (y/n):  ", clear_after=True).strip().lower()
        if replay == 'y':
            printer.erase_all_windows()
            play_game(Board(), printer, hard_mode, previous_answers, answer)
    user_input = printer.get_end_game_input(num_wins, num_games).strip().lower()
    while True:
        if user_input == 'r':
            printer.erase_all_windows()
            play_game(Board(), printer, hard_mode, previous_answers)
        elif user_input == 's':
            printer.show_answer(answer)
            user_input = printer.get_end_game_input(num_wins, num_games).strip().lower()
        elif user_input == 'q':
            quit()
        else:
            printer.show_invalid_end_game_input()
            user_input = printer.get_end_game_input(num_wins, num_games).strip().lower()


def main(stdscr) -> None:
    printer = WordlePrinter(stdscr)
    build_word_collections('allowed_guesses.txt', 'answers.txt')
    hard_mode = False
    if "-h" in sys.argv or "-hardMode" in sys.argv:
        hard_mode = True
    printer.show_startup_prompt(stdscr, hard_mode)
    play_game(Board(), printer, hard_mode, [])


if __name__ == '__main__':
    wrapper(main)
