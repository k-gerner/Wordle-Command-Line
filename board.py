
CORRECT, WRONG_SPOT, INCORRECT, UNGUESSED = 1, 2, 3, 4


class Board(object):
	"""Class representing the Wordle board, containing the guesses and the aggregate letter scores."""
	def __init__(self):
		self.guesses = []
		letters = {}
		for letter in 'abcdefghijklmnopqrstuvwxyz':
			letters[letter] = UNGUESSED
		self.letters = letters

	def add_guess(self, guess_obj):
		self.guesses.append(guess_obj)
		for index, letter in enumerate(guess_obj.word):
			# Update the "color" of the letter. Correct (green) will take priority over a wrong spot (yellow),
			# which will take priority over incorrect (red), etc.
			self.letters[letter] = min(self.letters[letter], guess_obj.scores[index])

	def guessed_already(self, word) -> bool:
		for guess in self.guesses:
			if guess.word == word:
				return True
		return False

	def most_recent_guess(self):
		assert len(self.guesses) >= 1, "There is no most recent guess!"
		return self.guesses[-1]

	def num_guesses(self):
		return len(self.guesses)

	def num_guesses_remaining(self):
		return 6 - len(self.guesses)


class Guess(object):
	"""Class representing a single guess, containing the word and the individual letter scores."""
	def __init__(self, word):
		self.word = word
		self.scores = [INCORRECT] * 5

	def set_score(self, index, score):
		self.scores[index] = score

	def get_inaccurate_indices(self):
		"""Gets a list of indices for which the letter was not correct. Includes WRONG_SPOT and INCORRECT"""
		incorrect_indices = []
		for index, score in enumerate(self.scores):
			if score != CORRECT:
				incorrect_indices.append(index)
		return incorrect_indices

	def is_correct(self):
		return len(self.get_inaccurate_indices()) == 0
