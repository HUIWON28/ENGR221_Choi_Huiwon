""" 
Author: Huiwon Choi
Last updated: September 20, 2026
Description: Stores the game state for Antarctic Survival, including the
board, player, food, enemies, movement, and game-over behavior.
"""

import random

from cell import Cell
from preferences import Preferences


class GameData:
    def __init__(self):
        # current state of the board
        self.board = [[Cell(row, col) for col in range(Preferences.NUM_COLS)]
                      for row in range(Preferences.NUM_ROWS)]

        # whether or not the game is over
        self.gameover = False

        # the current cell containing the player
        self.player = self.board[0][0]
        self.player.become_player()

        # The number of empty cells on the board, accounting for the player cell
        self.num_empty_cells = Preferences.NUM_CELLS - 1

        # A list of cells containing food
        self.food = []
        # Number of food eaten
        self.score = 0

        # A list of cells containing enemies
        self.enemies = []

    
    # game limits methods #
    def at_max_food(self) -> bool:
        """Check whether we can add more food."""
        return len(self.food) / self.num_empty_cells > Preferences.MAX_FOOD

    def at_max_enemies(self) -> bool:
        """Check whether we can add more enemies."""
        return len(self.enemies) / self.num_empty_cells > Preferences.MAX_ENEMIES

    def set_game_over(self) -> None:
        """Turn on the game over flag."""
        self.gameover = True

 
    # neighbor retrieval methods #
    def get_west_neighbor(self, cell: Cell) -> Cell:
        """return the cell immediately to the left or none at the edge"""
        if cell.get_col() > 0:
            return self.board[cell.get_row()][cell.get_col() - 1]
        return None

    def get_east_neighbor(self, cell: Cell) -> Cell:
        if cell.get_col() < Preferences.NUM_COLS - 1:
            return self.board[cell.get_row()][cell.get_col() + 1]
        return None

    def get_north_neighbor(self, cell: Cell) -> Cell:
        if cell.get_row() > 0:
            return self.board[cell.get_row() - 1][cell.get_col()]
        return None

    def get_south_neighbor(self, cell: Cell) -> Cell:
        if cell.get_row() < Preferences.NUM_ROWS - 1:
            return self.board[cell.get_row() + 1][cell.get_col()]
        return None

   
    # player movement methods #
    """find the neighbor in the desired direction"""
    def move_player_right(self) -> None:
        cell = self.get_east_neighbor(self.player)
        if cell is not None:
            self.move_player_to_cell(cell)

    def move_player_left(self) -> None:
        cell = self.get_west_neighbor(self.player)
        if cell is not None:
            self.move_player_to_cell(cell)

    def move_player_up(self) -> None:
        cell = self.get_north_neighbor(self.player)
        if cell is not None:
            self.move_player_to_cell(cell)

    def move_player_down(self) -> None:
        cell = self.get_south_neighbor(self.player)
        if cell is not None:
            self.move_player_to_cell(cell)

    def move_player_to_cell(self, cell: Cell) -> None:
        """move the player to the given cell"""
        if cell.is_food():
            self.eat_food(cell)
            self.update_player_cell(cell)
        elif cell.is_enemy():
            self.player.become_empty()
            self.set_game_over()
        else:
            self.update_player_cell(cell)

    def update_player_cell(self, new_cell: Cell) -> None:
        """move the player to the new cell"""
        self.player.become_empty()
        self.player = new_cell
        self.player.become_player()

   
    # food related methods #
    def add_food(self) -> None:
        """randomly select a row and column and add food to that cell if it is empty"""
        row = random.randrange(0, Preferences.NUM_ROWS)
        col = random.randrange(0, Preferences.NUM_COLS)
        cell = self.board[row][col]

        if cell.is_empty():
            cell.become_food()
            """add to food list"""
            self.food.append(cell)
            self.num_empty_cells -= 1

    def eat_food(self, cell: Cell) -> None:
        if cell in self.food:
            self.food.remove(cell)
            self.score += 1
            self.num_empty_cells += 1

      # enemy movement methods #
    def add_enemy(self) -> None:
        """add an enemy to the bottom right cell when possible"""
        cell = self.board[Preferences.NUM_ROWS - 1][Preferences.NUM_COLS - 1]

        """ check which type the cell contains """
        if cell.is_player():
            self.set_game_over()
        elif cell.is_food():
            self.eat_food(cell)
            cell.become_enemy()
            self.enemies.append(cell)
            self.num_empty_cells -= 1
        elif cell.is_empty():
            cell.become_enemy()
            self.enemies.append(cell)
            self.num_empty_cells -= 1

    def move_enemy_to_cell(self, enemy_cell: Cell, cell: Cell, idx: int) -> None:
        """move an enemy to a destination cell and update the game state"""
        if cell.is_player():
            self.set_game_over()
            return

        if cell.is_enemy():
            """not move"""
            return

        if cell.is_food():
            self.eat_food(cell)

        """move enemy from the old cell to the new cell"""
        enemy_cell.become_empty() 
        cell.become_enemy()
        self.enemies[idx] = cell

    # enemy movement methods(similarly to player movement methods) #
    def move_enemy_left(self, idx: int) -> None:
        """find the neighbor in the desired direction, if it possible move enemy at one cell to left"""
        enemy_cell = self.enemies[idx]
        cell = self.get_west_neighbor(enemy_cell)
        if cell is not None:
            self.move_enemy_to_cell(enemy_cell, cell, idx)

    def move_enemy_right(self, idx: int) -> None:
        enemy_cell = self.enemies[idx]
        cell = self.get_east_neighbor(enemy_cell)
        if cell is not None:
            self.move_enemy_to_cell(enemy_cell, cell, idx)

    def move_enemy_up(self, idx: int) -> None:
        enemy_cell = self.enemies[idx]
        cell = self.get_north_neighbor(enemy_cell)
        if cell is not None:
            self.move_enemy_to_cell(enemy_cell, cell, idx)

    def move_enemy_down(self, idx: int) -> None:
        enemy_cell = self.enemies[idx]
        cell = self.get_south_neighbor(enemy_cell)
        if cell is not None:
            self.move_enemy_to_cell(enemy_cell, cell, idx)


if __name__ == "__main__":
    gd = GameData()
    print(gd.get_west_neighbor(gd.player))
