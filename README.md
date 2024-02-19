# Wordle
> [!NOTE]
> From v2.0.0, this code uses the Python `curses` module for cleaner 
> command line printing. This is not available on Windows operating 
> systems. If you are using Windows, please use [v1.1.0][v1.1.0 release] instead.

A version of the newly popular game "Wordle" that is playable 
from the command line. It uses the same word lists as the 
official game! Lists found [here][allowed guesses] and 
[here][answers list].

<img src="/Images/sample_game_in_play.png" alt = "during the game" width="47%" align = "left">
<img src="/Images/sample_game_over.png" alt = "end of the game" width="47%">  

### How to play  
The objective of the game is to guess the five-letter word 
correctly in 6 tries. After each guess, you will be told 
which of the letters are in the word and if they are in the 
correct spot or not. 

To use, run the `wordle.py` file as follows:
```
> python3 wordle.py
```
You can also choose to enable hard mode by adding the command 
line argument `-h` or `-hardMode`. With hard mode enabled, 
if a letter is marked yellow or green, you must use it in all 
future guesses. 

The output will update in place. Once the user quits the 
program, the output will be cleared from the screen.

Here is an example of a full playthrough of Wordle using the
program, using regular mode, and then hard mode:

![][demo gif]

[allowed guesses]: https://gist.github.com/cfreshman/cdcdf777450c5b5301e439061d29694c
[answers list]: https://gist.github.com/cfreshman/a03ef2cba789d8cf00c08f767e0fad7b
[v1.1.0 release]: https://github.com/k-gerner/Wordle-Command-Line/releases/tag/v1.1.0
[demo gif]: https://github.com/k-gerner/gif-storage/blob/main/wordle/wordle_demo.gif