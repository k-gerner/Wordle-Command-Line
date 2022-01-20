import os
import random
from typing import List, Tuple

VALID_GUESSES = set() # all 5 letter words
POSSIBLE_ANSWERS = [] # all words that could still be valid guesses according to previous letter scores

CORRECT, WRONG_SPOT, INCORRECT, UNGUESSED = 1, 2, 3, 4

GREEN = '\033[92m' # green
YELLOW = "\u001b[38;5;226m" # yellow
WHITE = '\033[0m' # white
CYAN = "\033[36m" # cyan
RED = '\033[91m' # red

HISTORY_FILE = 'history.txt'

def build_word_collections(guesses_filename:str, answers_filename:str) -> None:
	'''Populates the VALID_GUESSES and POSSIBLE_ANSWERS collections'''
	global VALID_GUESSES, POSSIBLE_ANSWERS
	with open(guesses_filename, 'r') as guesses_file:
		for word in guesses_file:
			VALID_GUESSES.add(word.strip().lower())
	with open(answers_filename, 'r') as answers_file:
		for word in answers_file:
			POSSIBLE_ANSWERS.append(word.strip().lower())

def evaluate_guess(guess:str, answer:str) -> Tuple[List[int], bool]:
	'''Evaluates the guess and returns a score for each letter, and whether or not the guess was correct'''
	assert len(guess) == len(answer), "The guess could not be evaluated because it was not 5 letters long!"
	scores = [INCORRECT]*5
	modified_answer = answer
	incorrect_indexes = []
	# first check for all the correctly guessed letters
	# This must be done before checking for wrong spot / incorrect letters
	for i in range(len(guess)):
		if guess[i] == answer[i]:
			scores[i] = CORRECT
			modified_answer = modified_answer[:i] + "_" + modified_answer[i+1:]
		else:
			incorrect_indexes.append(i)
	if len(incorrect_indexes) == 0:
		return scores, True
	for i in incorrect_indexes:
		if guess[i] in modified_answer:
			scores[i] = WRONG_SPOT
			true_location = modified_answer.index(guess[i])
			modified_answer = modified_answer[:true_location] + "_" + modified_answer[true_location+1:]
	return scores, False

def get_user_guess(info_dict:dict) -> str:
	'''Gets the guess word from the user'''
	guess = input("Type your guess, or type 'i' for info about which letters remain:  ").strip().lower()
	while True:
		if guess == 'i':
			print_letters_info(info_dict)
			guess = input("Type your guess:  ").strip().lower()
		elif guess == 'q':
			print("Thanks for playing! Have a nice day!")
			quit()
		elif guess == "" or len(guess) != 5:
			guess = input("Must be 5 letters. Try again:  ").strip().lower()
		elif not guess.isalpha():
			guess = input("Must only contain letters. Try again:  ").strip().lower()
		elif guess not in VALID_GUESSES:
			guess = input("Not a valid word. Try again:  ").strip().lower()
		else:
			break
	return guess


def print_help_menu():
	'''Prints out instructions'''
	print("\nEach game, you have 6 tries to guess the 5 letter word.")
	print("After each guess, the letters you guessed will be color coded depending on whether or not they are in the word.")
	print("For example, if you typed 'codes', the output may look something like this:\n")
	print(f"{YELLOW}C {GREEN}O {WHITE}D E {GREEN}S{WHITE}\n")
	print("This would indicate that 'O' and 'S' are in the correct positions, 'C' is in the word, but not in the right spot, and 'D' & 'E' are not in the word.")
	print("Therefore, a smart next guess might be 'LOCKS' because 'O' and 'S' are in the same positions, and 'C' is in a different position.")
	print("Good luck!\n")


def print_letters_info(info_dict:dict) -> None:
	'''Prints out the letters colored accordingly'''
	print(f"{GREEN}Green{WHITE} = Correct spot\n" + 
		f"{YELLOW}Yellow{WHITE} = Incorrect spot\n" + 
		f"{RED}Red{WHITE} = Does not appear\n" + 
		"White = Unguessed\n")
	output = ""
	for letter in info_dict.keys():
		letter_status = info_dict[letter]
		if letter_status == CORRECT:
			color = GREEN
		elif letter_status == WRONG_SPOT:
			color = YELLOW
		elif letter_status == INCORRECT:
			color = RED
		else:
			color = WHITE
		output += f"{color}{letter.upper()}{WHITE} "
	print(output.strip() + '\n')


def print_words_with_color(words_list:List[str], scores_lists:List[List[int]]) -> None:
	'''Prints out the words with the letters color coded properly'''
	print()
	for word_index in range(len(words_list)):
		formatted_word = ""
		word = words_list[word_index].upper()
		scores = scores_lists[word_index]
		for letter_index in range(len(word)):
			letter = word[letter_index]
			letter_score = scores[letter_index]
			if letter_score == CORRECT:
				color = GREEN
			elif letter_score == WRONG_SPOT:
				color = YELLOW
			else:
				color = WHITE
			formatted_word += f"{color}{letter}{WHITE} "
		print(formatted_word.strip())
	print()


def tally_game(win:bool) -> Tuple[int, int]:
	'''
	Adds to the game history file to keep track of total wins across all runs
	Returns a tuple: (# wins, total games)
	'''
	num_wins = 1 if win else 0
	total_games = 1
	if os.path.isfile(HISTORY_FILE):
		with open(HISTORY_FILE, 'r') as file:
			num_wins += int(file.readline().strip())
			total_games += int(file.readline().strip())
	with open(HISTORY_FILE, 'w') as file:
		file.write(str(num_wins) + '\n')
		file.write(str(total_games) + '\n')
		file.write("# Do not modify. This file keeps track of the total # of wins and games you have played.\n")
		file.write("# If you delete this file, your past games history will be reset.")
	return num_wins, total_games
	


def main():
	os.system("") # allows colored terminal to work on Windows OS
	print("Welcome to Wordle!")
	build_word_collections('allowed_guesses.txt', 'answers.txt')
	user_input = input("Type 'h' for the help menu, or ENTER when you are ready to play!  ").strip().lower()
	if user_input == 'h':
		print_help_menu()
	else:
		print()
	replay_word = False
	previous_answers = []
	while True:
		letters_info = {}
		for letter in 'abcdefghijklmnopqrstuvwxyz':
			letters_info[letter] = UNGUESSED
		if replay_word:
			answer = previous_answers[-1]
			replay_word = False
		else:
			answer = random.choice(POSSIBLE_ANSWERS).lower()
			while answer in previous_answers:
				answer = random.choice(POSSIBLE_ANSWERS).lower()
			previous_answers.append(answer)
		previous_guesses = []
		previous_scores = []
		winning_turn = -1
		for turn in range(6):
			print("You have %d turn%s left!" % (6-turn, "s" if turn < 5 else ""))
			guess = get_user_guess(letters_info)
			scores, win = evaluate_guess(guess, answer)
			previous_guesses.append(guess)
			previous_scores.append(scores)
			# update_letters_info(letters_info, guess, scores)
			for i in range(5):
				letters_info[guess[i]] = min(letters_info[guess[i]], scores[i])
			print_words_with_color(previous_guesses, previous_scores)
			if win:
				winning_turn = turn + 1
				break
		num_wins, num_games = tally_game(winning_turn != -1)
		if winning_turn != -1:
			print("Congratulations! You guessed correctly in %d tr%s!" % (winning_turn, "ies" if winning_turn > 1 else "y"))
		else:
			replay = input("Looks like you didn't guess correctly!\nWould you like to replay with the same word? (y/n):  ").strip().lower()
			if replay == 'y':
				replay_word = True
				continue
		print("You have won %d of %d games (%d%%)" % (num_wins, num_games, int((num_wins/num_games) * 100)))
		print("Type one of the following options:")
		print("- 'r' for replay with a new word")
		print("- 's' to show the correct answer")
		print("- 'q' to quit")
		user_input = input("Which option will you choose?  ").strip().lower()
		while True:
			if user_input == 'r':
				break
			elif user_input == 's':
				print(f"The correct answer was: {CYAN}%s{WHITE}" % answer.upper())
				user_input = input("Which option will you choose?  ").strip().lower()
			elif user_input == 'q':
				print("Thanks for playing! Have a nice day!")
				quit()
			else:
				user_input = input("Invalid input. Try again:  ").strip().lower()


if __name__ == '__main__':
	main()



