# Word-Salad-Discord-Bot
Discord bot that allows multiple users to play word salad in a text channel


Current issues to address, in priority groups:

HIGH PRIORITY

-Add command to let players leave, and an option to let players vote someone out. Also add a way for VIP to remove players.

-Use embedded commands or another good solution to avoid the 2000-character limit. Remove the stopgap code being used to do that right now

-When you undo, it should reset whose turn it is

-Prevent people from having the same names

-What if there are multiple different two word melds or multiple different stealable words for an entry?


MEDIUM PRIORITY

-Make sure the bot doesn't interact with people who aren't playing (which means they can type single words with no interaction). Only let them use the "name" command.

-Prevent multiple simultaneous "end" commands. Potentially limit the "end" command (as well as ".play") to whoever is VIP

-Allow VIP handoff from one person to another

-Make the tilebag larger than the rest of the text

-Prevent people who aren't playing from voting

-Prevent the bot from doing the 2 min reminder for votes that were concurrent, so it doesn't clutter the chat. (Will require multi thread understanding.)

-Order the stats in descending score order

-Add VIP validation for undo command

-Prevent show during vote


LOW PRIORITY

-Change the "name" dialogue so it doesn't tell people to enter ".play" if they're already playing

-Maybe change the length of the game based on how many people are playing. Could even add a speed game with fewer tiles. Basically, would have the same distribution but not use 
all of the tiles.

-Change scoring to score of a word being #letters minus 2

-Validate against fucky wucky names

-Add more fun stats like number of steals per player, number of steals overall, etc.

-3+ word melds
