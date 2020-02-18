# River Crossing  

*Another day, another ISS assignment.*

**River Crossing** is a simple multiplayer turn-based arcade game (totally not a rip-off of Crossy Road) written using Python, the PyGame library, and an unhealthy amount of coffee.  

Help the ghosts cross a river filled with turtles, crabs, orcas, boats, and whales (yes, whales in a river) without dying. Beat your opponent to it in the least time to win the round.  

## Instructions  

Get to the other bank without crashing into enemies. Fast.  

### Controls  

Controls for Player 1:  
UP : Up Arrow  
DOWN : Down Arrow  
LEFT : Left Arrow  
RIGHT : Right Arrow  

Controls for Player 2:  
UP : W Key  
DOWN : S Key  
LEFT : A Key  
RIGHT : D Key  

### Scoring  

Player gains 10 points for successfully getting past every moving enemy, and 5 points for getting past every static enemy. Also, a time bonus may be added to the score depending on how fast the player manages to successfully cross the river.  
Results of the round is decided based on the scores. The winner progresses to the next level, and their enemies speed up.  
  
Good luck getting past level 10.

## Functional and Technical details  

* Game map consists of a river with over five partitions in it.  
* There are 2 players in the game, only one of them playing at any given point of time.  
* There are two types of obstacles, moving and static.  
* Players die when they hit an obstacle.  
* The score is shown on the screen at all times and gets updated as the round progresses.  
* The code conforms to PEP8 guidelines.  
* Strings, fonts and constants for objects are defined in individual config files.
