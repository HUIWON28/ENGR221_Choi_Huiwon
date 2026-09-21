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
        # The current state of the board
        self.board = [[Cell(row, col) for col in range(Preferences.NUM_COLS)]
                      for row in range(Preferences.NUM_ROWS)]

        # Whether or not the game is over
        self.gameover = False

        # The current cell containing the player
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

    #######################
    # Game Limits Methods #
    #######################

    def at_max_food(self) -> bool:
        """Check whether we can add more food."""
        return len(self.food) / self.num_empty_cells > Preferences.MAX_FOOD

    def at_max_enemies(self) -> bool:
        """Check whether we can add more enemies."""
        return len(self.enemies) / self.num_empty_cells > Preferences.MAX_ENEMIES

    def set_game_over(self) -> None:
        """Turn on the game over flag."""
        self.gameover = True

    ##############################
    # Neighbor Retrieval Methods #
    ##############################

    def get_west_neighbor(self, cell: Cell) -> Cell:
        """Return the cell immediately to the left, or None at the edge."""
        if cell.get_col() > 0:
            return self.board[cell.get_row()][cell.get_col() - 1]
        return None

    def get_east_neighbor(self, cell: Cell) -> Cell:
        """Return the cell immediately to the right, or None at the edge."""
        if cell.get_col() < Preferences.NUM_COLS - 1:
            return self.board[cell.get_row()][cell.get_col() + 1]
        return None

    def get_north_neighbor(self, cell: Cell) -> Cell:
        """Return the cell immediately above, or None at the edge."""
        if cell.get_row() > 0:
            return self.board[cell.get_row() - 1][cell.get_col()]
        return None

    def get_south_neighbor(self, cell: Cell) -> Cell:
        """Return the cell immediately below, or None at the edge."""
        if cell.get_row() < Preferences.NUM_ROWS - 1:
            return self.board[cell.get_row() + 1][cell.get_col()]
        return None

    ###########################
    # Player Movement Methods #
    ###########################

    def move_player_right(self) -> None:
        """Move the player one cell to the right if possible."""
        cell = self.get_east_neighbor(self.player)
        if cell is not None:
            self.move_player_to_cell(cell)

    def move_player_left(self) -> None:
        """Move the player one cell to the left if possible."""
        cell = self.get_west_neighbor(self.player)
        if cell is not None:
            self.move_player_to_cell(cell)

    def move_player_up(self) -> None:
        """Move the player one cell up if possible."""
        cell = self.get_north_neighbor(self.player)
        if cell is not None:
            self.move_player_to_cell(cell)

    def move_player_down(self) -> None:
        """Move the player one cell down if possible."""
        cell = self.get_south_neighbor(self.player)
        if cell is not None:
            self.move_player_to_cell(cell)

    def move_player_to_cell(self, cell: Cell) -> None:
        """Move the player to the given cell."""
        if cell.is_food():
            self.eat_food(cell)
            self.update_player_cell(cell)
        elif cell.is_enemy():
            self.player.become_empty()
            self.set_game_over()
        else:
            self.update_player_cell(cell)

    def update_player_cell(self, new_cell: Cell) -> None:
        """Move the player to the new cell."""
        self.player.become_empty()
        self.player = new_cell
        self.player.become_player()

    ########################
    # Food Related Methods #
    ########################

    def add_food(self) -> None:
        """Add food to a random open spot on the board."""
        row = random.randrange(0, Preferences.NUM_ROWS)
        col = random.randrange(0, Preferences.NUM_COLS)
        cell = self.board[row][col]

        if cell.is_empty():
            cell.become_food()
            self.food.append(cell)
            self.num_empty_cells -= 1

    def eat_food(self, cell: Cell) -> None:
        """Remove the food from a cell and increase the score."""
        if cell in self.food:
            self.food.remove(cell)
            self.score += 1
            self.num_empty_cells += 1

    ##########################
    # Enemy Movement Methods #
    ##########################

    def add_enemy(self) -> None:
        """Add an enemy to the bottom-right corner when possible."""
        cell = self.board[Preferences.NUM_ROWS - 1][Preferences.NUM_COLS - 1]

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

    def move_enemy_to_cell(self, enemy_cell: Cell,
                           cell: Cell, idx: int) -> None:
        """Move an enemy to a destination cell and update the game state."""
        if cell.is_player():
            self.set_game_over()
            return

        if cell.is_enemy():
            return

        if cell.is_food():
            self.eat_food(cell)

        enemy_cell.become_empty()
        cell.become_enemy()
        self.enemies[idx] = cell

    def move_enemy_left(self, idx: int) -> None:
        """Move the enemy at index idx one cell left if possible."""
        enemy_cell = self.enemies[idx]
        cell = self.get_west_neighbor(enemy_cell)
        if cell is not None:
            self.move_enemy_to_cell(enemy_cell, cell, idx)

    def move_enemy_right(self, idx: int) -> None:
        """Move the enemy at index idx one cell right if possible."""
        enemy_cell = self.enemies[idx]
        cell = self.get_east_neighbor(enemy_cell)
        if cell is not None:
            self.move_enemy_to_cell(enemy_cell, cell, idx)

    def move_enemy_up(self, idx: int) -> None:
        """Move the enemy at index idx one cell up if possible."""
        enemy_cell = self.enemies[idx]
        cell = self.get_north_neighbor(enemy_cell)
        if cell is not None:
            self.move_enemy_to_cell(enemy_cell, cell, idx)

    def move_enemy_down(self, idx: int) -> None:
        """Move the enemy at index idx one cell down if possible."""
        enemy_cell = self.enemies[idx]
        cell = self.get_south_neighbor(enemy_cell)
        if cell is not None:
            self.move_enemy_to_cell(enemy_cell, cell, idx)


if __name__ == "__main__":
    gd = GameData()
    print(gd.get_west_neighbor(gd.player))
