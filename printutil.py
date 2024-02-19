import curses

ALERT_SYMBOL = "<!>"


class PrintMode(object):
	DEFAULT = 0
	INFO = 1
	ERROR = 2


class Colors(object):
	DEFAULT = 0
	RED = 197
	YELLOW = 227
	GREEN = 47
	CYAN = 52
	GREY = 251

	def __init__(self):
		curses.start_color()
		curses.use_default_colors()
		for i in range(0, curses.COLORS):
			curses.init_pair(i + 1, i, -1)
		self.color_ids = {Colors.DEFAULT, Colors.RED, Colors.YELLOW, Colors.GREEN, Colors.CYAN, Colors.GREY}

	def get(self, color_int):
		if color_int not in self.color_ids:
			return curses.color_pair(Colors.DEFAULT)
		return curses.color_pair(color_int)


def get_input(window, r, c, prompt_string, color=0) -> str:
	"""Reads the input from the user"""
	curses.echo()
	window.addstr(r, c, prompt_string, color)
	window.refresh()
	user_input = window.getstr(r + 1, 0).decode(encoding="utf-8")
	window.erase()
	window.refresh()
	return user_input  # ^^^^  reading input at next line


def cprint_lines(window, start_r, c, strings, refresh=False, color=0) -> int:
	"""
	Print a list of strings, with each string being on a new line.
	Returns the number of the row below the last printed row.
	"""
	r = start_r
	for s in strings:
		cprint(window, r, c, s, refresh=False, color=color)
		r += 1
	if refresh:
		window.refresh()
	return r


def cprint(window, r, c, string, refresh=False, color=0) -> int:
	"""
	Print the given string at a location. Optionally refreshes the screen.
	Returns the number of the column right of the last printed char.
	"""
	window.addstr(r, c, string, color)
	if refresh:
		window.refresh()
	return c + len(string)
