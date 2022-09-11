# Wordle
A version of the newly popular game "Wordle" that is playable 
from the command line. It uses the same word lists as the 
official game! Lists found [here](https://gist.github.com/cfreshman/cdcdf777450c5b5301e439061d29694c) 
and [here](https://gist.github.com/cfreshman/a03ef2cba789d8cf00c08f767e0fad7b).

### How to play  
The objective of the game is to guess the five-letter word 
correctly in 6 tries. After each guess, you will be told 
which of the letters are in the word and if they are in the 
correct spot or not. 

By default, the output will update in place. However, if you 
would like to preserve all output to the terminal, you can 
add the command line argument `-e` or `-eraseModeOff` when 
starting the program.

Here is an example of a full playthrough of one round of 
Wordle:

**With eraseMode ON:**

<img src="https://github.com/k-gerner/Wordle-Command-Line/blob/main/Images/duringPlay_eraseModeOn.png" alt = "during the game" width="50%" align = "left">
<img src="https://github.com/k-gerner/Wordle-Command-Line/blob/main/Images/gameOver_eraseModeOn.png" alt = "end of the game" width="45%">  

**With eraseMode OFF:**

<img src="https://github.com/k-gerner/Wordle-Command-Line/blob/main/Images/sampleGamePlaythrough_eraseModeOff.png" alt = "playthrough on terminal" width="90%" align = "left"> 
