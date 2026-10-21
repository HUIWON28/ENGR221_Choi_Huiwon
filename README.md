# ENGR 221
Name: Huiwon Choi  
Course: ENGR 221 - Data Structures and Algorithms in Python  
Semester: Fall 2026

# Duck Collector (BFS / DFS)

A Snake-style game where a horse collects ducks that then follow it. 
AI mode uses breadth-first search (BFS) or depth-first search (DFS) to find the closest duck.

## Files
- `game_data.py` (modified): game state, player movement
  (`move_player_to_cell`), and AI (`get_next_cell_ai`, `get_first_cell_in_path`).
  Also changed `ate_food` to add the new head to the front of the body list.
- `search_structure.py` (modified): custom `Stack` (LIFO) and `Queue` (FIFO).
- `answers.txt` (added): answers to the homework questions.
- `cell.py`: a single board cell (not modified).
- `controller.py`: game loop and key handling (not modified).
- `display.py`: draws the board with pygame (not modified).
- `preferences.py`: constant values used across the game (not modified).
- `tests/structures_tests.py`: pytest tests for Stack and Queue.

## How to run
Install dependencies: `pip install pygame pytest`
Run the game from the `Lab4` folder: controller.py
- Press any key to start. Move with the arrow keys (or i/j/k/l).
- Press `a` to switch to AI mode.
- For DFS, run `Controller("dfs").run()` at the bottom of `controller.py` (default is BFS).

Run the tests:
pytest -v -m stack tests/structures_tests.py
pytest -v -m queue tests/structures_tests.py