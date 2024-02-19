from board import CORRECT, WRONG_SPOT, INCORRECT, UNGUESSED
import printutil as pu
import curses

INCORRECT_BOARD_LETTER_COLOR = 5


class WordlePrinter(object):

	def __init__(self, screen):
		self.screen = screen
		self.colors = pu.Colors()
		self.color_map = {
			CORRECT: self.colors.get(self.colors.GREEN),
			WRONG_SPOT: self.colors.get(self.colors.YELLOW),
			INCORRECT: self.colors.get(self.colors.RED),
			UNGUESSED: self.colors.get(self.colors.DEFAULT),
			INCORRECT_BOARD_LETTER_COLOR: self.colors.get(self.colors.GREY)
		}
		self.hard_mode_indicator_window = curses.newwin(1, 50, 0, 0)
		self.color_meanings_window = curses.newwin(4, 50, 2, 0)
		self.guesses_window = curses.newwin(6, 20, 7, 0)
		self.letter_list_window = curses.newwin(1, 55, 14, 0)
		self.guesses_remaining_window = curses.newwin(1, 100, 16, 0)
		self.user_input_window = curses.newwin(2, 100, 18, 0)
		self.end_game_input_window = curses.newwin(7, 100, 18, 0)
		self.show_answer_window = curses.newwin(1, 100, 25, 0)
		self.windows = [
			self.hard_mode_indicator_window,
			self.color_meanings_window,
			self.guesses_window,
			self.letter_list_window,
			self.guesses_remaining_window,
			self.user_input_window,
			self.end_game_input_window,
			self.show_answer_window
		]

	def show_help(self, hard_mode):
		"""Show the rules of the game"""
		self.screen.clear()
		output_lines = [
			"Each game, you have 6 tries to guess the 5 letter word.",
			"After each guess, the letters you guessed will be color ",
			"coded depending on whether or not they are in the word.",
			"For example, if you typed 'codes', the output may look ",
			"something like this:"
		]
		row_num = pu.cprint_lines(self.screen, 1, 0, output_lines)
		col = 0
		col = pu.cprint(self.screen, row_num, col, "C ", color=self.colors.get(self.colors.YELLOW))
		col = pu.cprint(self.screen, row_num, col, "O ", color=self.colors.get(self.colors.GREEN))
		col = pu.cprint(self.screen, row_num, col, "D E ", color=self.colors.get(self.colors.DEFAULT))
		pu.cprint(self.screen, row_num, col, "S", color=self.colors.get(self.colors.GREEN))
		row_num += 1
		output_lines = [
			"This would indicate that 'O' and 'S' are in the correct",
			"positions, 'C' is in the word, but not in the right spot,",
			"and 'D' & 'E' are not in the word.",
			"Therefore, a smart next guess might be 'LOCKS' because 'O'",
			"and 'S' are in the same positions, and 'C' is in a different",
			"position."
		]
		row_num = pu.cprint_lines(self.screen, row_num, 0, output_lines)
		if hard_mode:
			output_lines = [
				"Since you are in hard mode, you must use all valid letters",
				"from previous guesses in your future guesses."
			]
			row_num = pu.cprint_lines(self.screen, row_num, 0, output_lines)
		pu.cprint(self.screen, row_num, 0, "Good luck!")
		pu.cprint(self.screen, row_num + 1, 0, "Press any key to continue.", refresh=True)
		self.screen.getch()
		self.screen.clear()
		self.screen.refresh()

	def show_all_windows(self, board):
		# show color meanings at top
		# game board in middle
		# colored letter list (each letter is shown)
		# prompt at bottom
		self.paint_color_meanings()
		self.paint_guesses(board)
		self.paint_letter_list(board)
		self.paint_guesses_remaining(board)
		self.end_game_input_window.clear()  # hide the end game input window if it was displayed
		self.show_answer_window.clear()  # hide the previous answer if it was displayed
		self.refresh_windows()

	def update_board(self, board):
		"""Redisplay the guesses board and the guesses remaining string"""
		self.paint_guesses(board)
		self.paint_guesses_remaining(board)
		self.guesses_window.refresh()
		self.guesses_remaining_window.refresh()

	def paint_color_meanings(self):
		"""Paint the meanings of each color"""
		col = 0
		col = pu.cprint(self.color_meanings_window, 0, col, "Green", color=self.color_map[CORRECT])
		pu.cprint(self.color_meanings_window, 0, col, " = Correct spot")
		col = pu.cprint(self.color_meanings_window, 1, 0, "Yellow", color=self.color_map[WRONG_SPOT])
		pu.cprint(self.color_meanings_window, 1, col, " = Incorrect spot")
		col = pu.cprint(self.color_meanings_window, 2, 0, "Red", color=self.color_map[INCORRECT])
		pu.cprint(self.color_meanings_window, 2, col, " = Does not appear")
		pu.cprint(self.color_meanings_window, 3, 0, "White = Unguessed")

	def paint_guesses(self, board):
		"""Paint the game board guesses"""
		guesses_remaining = 6
		for guess in board.guesses:
			r = 6 - guesses_remaining
			for index, letter in enumerate(guess.word):
				c = 2 * index
				letter_score = guess.scores[index]
				if letter_score == INCORRECT:
					letter_score = INCORRECT_BOARD_LETTER_COLOR
				pu.cprint(self.guesses_window, r, c, letter, color=self.color_map[letter_score])
			guesses_remaining -= 1
		# paint the empty rows
		for num_rows_from_bottom in range(guesses_remaining):
			r = 6 - num_rows_from_bottom - 1  # -1 because arrays are zero-indexed
			pu.cprint(self.guesses_window, r, 0, "_ _ _ _ _")

	def paint_letter_list(self, board):
		"""Paint the current status of each letter in the alphabet"""
		c = 0
		for letter, score in board.letters.items():
			pu.cprint(self.letter_list_window, 0, c, letter, color=self.color_map[score])
			c += 2

	def paint_guesses_remaining(self, board):
		"""Paint the number of guesses remaining"""
		self.guesses_remaining_window.clear()
		guesses_remaining = 6 - len(board.guesses)
		if guesses_remaining == 1:
			text = "You have 1 guess remaining!"
		else:
			text = "You have %d guesses remaining!" % guesses_remaining
		pu.cprint(self.guesses_remaining_window, 0, 0, text)

	def show_win_message(self, board):
		winning_turn = len(board.guesses)
		text = "Congratulations! You guessed correctly in %d %s!" % (
			winning_turn, "tries" if winning_turn > 1 else "try")
		pu.cprint(self.guesses_remaining_window, 0, 0, text)
		self.guesses_remaining_window.refresh()

	def show_loss_message(self):
		text = "Looks like you didn't guess correctly!"
		pu.cprint(self.guesses_remaining_window, 0, 0, text)
		self.guesses_remaining_window.refresh()

	def get_input(self, text, print_mode=pu.PrintMode.DEFAULT, clear_after=False):
		text_start_col = 0
		if print_mode == pu.PrintMode.ERROR:
			pu.cprint(self.user_input_window, 0, 0, pu.ALERT_SYMBOL, color=self.colors.get(self.colors.RED))
			text_start_col = len(pu.ALERT_SYMBOL) + 1
		if print_mode == pu.PrintMode.INFO:
			pu.cprint(self.user_input_window, 0, 0, pu.ALERT_SYMBOL, color=self.colors.get(self.colors.CYAN))
			text_start_col = len(pu.ALERT_SYMBOL) + 1
		user_input = pu.get_input(self.user_input_window, 0, text_start_col, text)
		if clear_after:
			self.user_input_window.clear()
			self.user_input_window.refresh()
		return user_input

	def get_end_game_input(self, num_wins, num_games):
		"""Print the end game options and prompt the user for input"""
		percent_games_won = int((num_wins / num_games) * 100)
		output_lines = [
			"You have won %d of %d games (%d%%)" % (num_wins, num_games, percent_games_won),
			"Type one of the following options:",
			"- 'r' to replay with a new word",
			"- 's' to show the correct answer",
			"- 'q' to quit"
		]
		row_num = pu.cprint_lines(self.end_game_input_window, 0, 0, output_lines)
		return pu.get_input(self.end_game_input_window, row_num, 0, "Which option will you choose?  ")

	def show_invalid_end_game_input(self):
		"""
		Use when the user is at the end game input prompt, and enters invalid input.
		Displays in the same location as the "show answer" result would print
		"""
		self.show_answer_window.clear()
		pu.cprint(self.show_answer_window, 0, 0, pu.ALERT_SYMBOL, color=self.colors.get(self.colors.RED))
		text_start_col = len(pu.ALERT_SYMBOL) + 1
		pu.cprint(self.show_answer_window, 0, text_start_col, "Invalid input.")
		self.show_answer_window.refresh()

	def show_answer(self, answer):
		"""Show the correct answer"""
		self.show_answer_window.clear()
		col = pu.cprint(self.show_answer_window, 0, 0, "The correct answer was: ")
		pu.cprint(self.show_answer_window, 0, col, answer.upper(), color=self.colors.get(self.colors.CYAN))
		self.show_answer_window.refresh()

	def show_hard_mode_indicator(self):
		"""Display an indicator at the top of the screen that the game is in hard mode"""
		self.hard_mode_indicator_window.clear()
		pu.cprint(self.hard_mode_indicator_window, 0, 0, pu.ALERT_SYMBOL, color=self.colors.get(self.colors.CYAN))
		text_start_col = len(pu.ALERT_SYMBOL) + 1
		text = "You are playing in hard mode!"
		pu.cprint(self.hard_mode_indicator_window, 0, text_start_col, text)
		self.hard_mode_indicator_window.refresh()

	def show_startup_prompt(self, stdscr, hard_mode):
		"""Show the help menu if the user requests it"""
		text = "Type 'h' for the help menu, or ENTER when you are ready to play!"
		user_input = pu.get_input(stdscr, 1, 0, text).strip().lower()
		if user_input == 'h':
			self.show_help(hard_mode)
		if hard_mode:
			self.show_hard_mode_indicator()

	def refresh_windows(self):
		for w in self.windows:
			w.refresh()

	def erase_all_windows(self):
		for w in self.windows:
			w.erase()
			w.refresh()
