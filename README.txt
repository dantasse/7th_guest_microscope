Trying to solve the Microscope puzzle from the Seventh Guest.

Google around, there's a lot more information about the puzzle. Particularly
this site is great if you just want to solve the damn thing:
http://analogbit.com/software/infection_ai/

Usage of this code: put your current board state in the microscope.py code,
towards the bottom, run it, and it will tell you your next move. Repeat until
you win. Sorry that's really frustrating and slow :P

Rumor around the internet is that the AI uses 3-ply deep search, so if you
always set search_depth=4, you should win. The problem is that takes forever,
partially because it's a wide search space, partially because my code is crummy.

Easy optimization (TODO) avoid computing simple_value all the time, maybe cache
it and update every time you make a move.
Slightly harder optimization would be to make a quicker way to duplicate the
board? It spends a ton of time copying arrays.
But I solved it so I'm done for now.
