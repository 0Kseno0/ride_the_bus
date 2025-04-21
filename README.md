# Schedule 1 - Ride The Bus
## ToDo:
Change position of buttons to relative values instead of absolute, right now they are for 1920x1080 monitors. Until then you could change the values according to your monitor using the pyautogui.position() loop.
Make script change value of how much you are betting in the case that you are low on money and just started playing the game (you should bet 4% of your money when going all the way, 10% when forfeiting at the third stage).
<hr>
This repository is a script that plays Ride The Bus on it's own.
<br>
All you need to do is go into the casino, interact with the ride the bus table, choose the amount of money you want to bet and start the program using an IDE (I am using PyCharm). From there it will keep playing until you stop the program.
<hr>
<strong>Fun fact</strong>, your customers will NOT seek you out for a deal while you are playing ride the bus. Though the moment you back out of the minigame, a customer will spawn in the casino for some weed if you have been at the table for a while.
<hr>
<br>
The script will not change the value of how much money you want to bet. 
<br>
Make sure Schedule 1 is on your main monitor for this to work properly (or you can adjust the position of the buttons/card region. You can easily get the position of your mouse using pyautogui.position() in a loop). 
