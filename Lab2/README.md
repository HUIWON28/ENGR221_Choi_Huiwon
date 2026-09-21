# ENGR 221 Lab 2 - Antarctic Survival

## Description
This Lab 2 project implements the Antarctic Survival game using pygame-ce.
The player moves around a 10x10 board, eats fish to increase the score,
and avoids seals. Food and enemies are added according to the game rules
provided in Homework 2.

## Files
- `gameData.py` - Game state and the methods implemented for Homework 2.
- `controller.py` - Runs the game, handles keyboard input, and advances cycles.
- `boardDisplay.py` - Draws the board and game graphics.
- `cell.py` - Represents an individual board cell.
- `preferences.py` - Stores constants, timing, colors, and image paths.
- `part1.txt` - Answers to Part 1 questions.
- `pseudocode.txt` - Pseudocode for the implemented methods.
- `images/` - Player, food, and enemy graphics.

## Controls
- Up arrow / I: move up
- Down arrow / K: move down
- Left arrow / J: move left
- Right arrow / L: move right

## How to run
1. Activate the ENGR 221 virtual environment.
2. Install pygame-ce:
   `py -m pip install pygame-ce`
3. From the `Lab2` directory, run:
   `py controller.py`

## Homework 2 implementation
Implemented:
- Neighbor retrieval
- Player movement
- Adding and eating food
- Adding and moving enemies
- Game-over behavior
- Function documentation and file header

## Customization
The project includes the provided graphical assets in the `images` directory.
For the required customization portion, replace the player, fish, and/or seal
PNG files (or update the corresponding paths in `preferences.py`) and be
prepared to explain what was changed during the lab demo.

## GitHub
From the ENGR221 repository directory:
```bash
git add --all
git commit -m "Lab 2 commit"
git push
```
