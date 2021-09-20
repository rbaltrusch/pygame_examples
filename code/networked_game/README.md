# Networked game

This is a short draft of a networked game, which can be played over a local network (only machines on the same network can join) on port 5555 (generally a free port to use).

# How to use

1) One machine needs to run the server.py script (this will keep running and answer any connected clients until the script is stopped).
1) One machine (this can be the machine running the server) runs the keys.py script, which opens a small pygame window recording keystrokes from the arrow keys and sends them to the server.
1) One machine (this can be the machine running the server) runs the game.py script, which opens a simple pygame window with a single picture of a cat. This script receives the speed at which this cat should be moved from the server.

The client.py script just provides the utility class `Network`, which is used to connect to the server.

# Sources

This short test game was written with the help of the Youtube Channel [Tech with Tim](https://www.youtube.com/watch?v=_fx7FQ3SP0U) and the accompanying [tutorial writeup](https://www.techwithtim.net/tutorials/python-online-game-tutorial/client/), which is linked to in the description under each video in the tutorial series.
