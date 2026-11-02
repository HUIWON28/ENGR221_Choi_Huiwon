""" TODO
Author: huiwon choi
Description:  Stores and updates the state of the Duck Collector game (board, player body, food, score). 
Includes player movement (growing when food iseaten) and the AI that uses BFS or DFS to find the closest food.
"""

import random
from enum import Enum, auto

from cell import Cell
from preferences import Preferences
from search_structure import Queue, Stack

class GameData:
    def __init__(self, ai_type):
        # the current state of the board
        self.board = [[Cell(row, col) for col in range(Preferences.NUM_COLS)] 
                                 for row in range(Preferences.NUM_ROWS)]

        # whether or not the game is over
        self.gameover = False

        # the current movement mode
        self.current_mode = self.MoveMode.GOING_EAST

        # the AI type to run
        self.ai_type = ai_type

        # a list of cells containing food
        self.food = []

        # a list of cells containing the body
        self.body = self.init_player()

        # number of food eaten
        self.score = 0


    # initialization methods #

    def init_player(self):
        """ initialize the player cell """

        # Get the top left cell
        player = self.get_cell(0,0)
        # Convert it to the player
        player.become_player()
        # Return a list with the player cell
        return [player]


    # get information about the board #

    def in_ai_mode(self):
        """ returns whether or not we are in AI mode """

        return self.current_mode == self.MoveMode.AI_MODE
    
    def get_cell(self, row, col):
        """ returns the cell at the given row and column """

        if (row >= 0 and row < Preferences.NUM_ROWS) and \
                (col >= 0 and col < Preferences.NUM_COLS):
            return self.board[row][col]
        # Implied else
        raise Exception('get_cell() tried to access cell outside of board: ({}, {})'.format(
            row, col))
    
    def get_player(self):
        """ returns the head of the body list """

        return self.body[0]
    
    def get_tail(self):
        """ returns the end of the body list """

        return self.body[-1]
    
    def at_max_food(self) -> bool:
        """ check whether we can add more food """

        return len(self.food) / Preferences.NUM_CELLS > Preferences.MAX_FOOD


    # set information about the board #

    def set_game_over(self) -> None:
        """ turn on the game over flag """
        self.gameover = True

    def set_going_north(self) -> None:
        """ set the mode to north """
        self.current_mode = self.MoveMode.GOING_NORTH 

    def set_going_south(self) -> None:
        """ set the mode to south """
        self.current_mode = self.MoveMode.GOING_SOUTH 

    def set_going_east(self) -> None: 
        """ set the mode to east """
        self.current_mode = self.MoveMode.GOING_EAST 

    def set_going_west(self) -> None:
        """ set the mode to west """
        self.current_mode = self.MoveMode.GOING_WEST 

    def set_ai_mode(self) -> None:
        """ set the mode to AI mode """
        self.current_mode = self.MoveMode.AI_MODE


    # find neighbors methods #

    def get_next_cell(self):
        """ returns the next cell to move to based on the current direction """
        return {
            self.MoveMode.GOING_NORTH : self.get_north_neighbor(self.get_player()),
            self.MoveMode.GOING_SOUTH : self.get_south_neighbor(self.get_player()),
            self.MoveMode.GOING_WEST : self.get_west_neighbor(self.get_player()),
            self.MoveMode.GOING_EAST : self.get_east_neighbor(self.get_player())
        }.get(self.current_mode)
    
    def get_west_neighbor(self, cell: Cell) -> Cell:
        """ returns the cell immediately to the left of the given cell. 
            If we are at the boundary, return None. """
            
        if cell.get_col() - 1 < 0:
            return None 
        else:
            return self.board[cell.get_row()][cell.get_col()-1]
        
    def get_east_neighbor(self, cell: Cell) -> Cell:
        """ returns the cell immediately to the right of the given cell.
            if we are at the edge of the map, return None. """
        
        if cell.get_col() + 1 >= Preferences.NUM_COLS:
            return None 
        else:
            return self.board[cell.get_row()][cell.get_col()+1]
    
    def get_north_neighbor(self, cell: Cell) -> Cell:
        """ returns the cell immediately above the given cell.
            if we are at the edge of the map, return None. """
        
        if cell.get_row() - 1 < 0:
            return None 
        else:
            return self.board[cell.get_row()-1][cell.get_col()]
        
    def get_south_neighbor(self, cell: Cell) -> Cell:
        """ returns the cell immediately below the given cell.
            if we are at the edge of the map, return None. """
        
        if cell.get_row() + 1 >= Preferences.NUM_ROWS:
            return None 
        else:
            return self.board[cell.get_row()+1][cell.get_col()]
        
    def get_neighbors(self, center: Cell):
        """ get all valid neighbors surrounding the center cell.
            always returns a list in order north, south, east, west """
        
        return list(filter(lambda x: x is not None, 
                [self.get_north_neighbor(center),
                self.get_south_neighbor(center),
                self.get_east_neighbor(center),
                self.get_west_neighbor(center)]))
    
    def get_random_neighbor(self, center: Cell) -> Cell:
        """ get a random neighbor from the given cell """

        neighbors = self.get_neighbors(center)
        return random.choice(neighbors)


    # player movement Methods #

    def move_player(self) -> None:
        """ move the player to the next step based on the current
            direction or as directed by AI """
        
        if self.in_ai_mode():
            next_cell = self.get_next_cell_ai()
        else:
            next_cell = self.get_next_cell()
        # move the snake to the next cell
        self.move_player_to_cell(next_cell)

    def move_player_left(self) -> None:
        """ move the player one cell to the left if it is empty """
        neighbor = self.get_west_neighbor(self.player)
        if neighbor:
            self.move_player_to_cell(neighbor)
        
    def move_player_right(self) -> None:
        """ move the player one cell to the right if it is empty """
        neighbor = self.get_east_neighbor(self.player)
        if neighbor:
            self.move_player_to_cell(neighbor)

    def move_player_up(self) -> None:
        """ move the player one cell up if it is empty """
        neighbor = self.get_north_neighbor(self.player)
        if neighbor:
            self.move_player_to_cell(neighbor)

    def move_player_down(self) -> None:
        """ move the player one cell down if it is empty """
        neighbor = self.get_south_neighbor(self.player)
        if neighbor:
            self.move_player_to_cell(neighbor)

    def move_player_to_cell(self, cell: Cell) -> None:
        """ move the player to the given cell. If the cell is off the map or
            part of the body, the game is over. If the cell is food, the player
            eats it and grows by one (the tail stays put). if the cell is empty,
            the player moves forward and the tail cell is freed. """

        # if the cell is a body or off the map, game over
        if not cell or cell.is_body():
            self.set_game_over()

        elif cell.is_food():
            # eat the food: it becomes the new head and the tail stays in place
            self.ate_food(cell)

        else:
            # empty cell: the old head becomes body, the new cell becomes head
            self.get_player().become_body()
            cell.become_player()
            self.body.insert(0, cell)
            # remove the tail so the length stays the same
            tail = self.body.pop()
            tail.become_empty()


    # food Related Methods #

    def add_food(self) -> None:
        """ adds food to a open spot on the board """

        # find a row on the board
        row = random.randrange(0, Preferences.NUM_ROWS)
        # find a col on the board
        col = random.randrange(0, Preferences.NUM_COLS)
        # get the cell at that location
        cell = self.get_cell(row, col)

        # if it is empty, add food
        if cell.is_empty():
            cell.become_food()
            self.food.append(cell)

    def ate_food(self, food_cell: Cell) -> None:
        """ eat the food """

        # change the current head to a body
        self.get_player().become_body()

        # the food becomes the new player
        food_cell.become_player()
        # add the new cell to the front of the body (index 0 is the head)
        self.body.insert(0, food_cell)
        # remove the cell from the food list
        self.food.remove(food_cell)

        # increment the player's score
        self.score += 1

    # AI methods #

    def get_next_cell_ai(self) -> Cell:
        """ search the board (BFS or DFS depending on ai_type) for the nearest
            reachable food. returns the first cell the player should step on
            along the path to that food. If no food is reachable, returns a
            safe neighbor, or a random neighbor as a last resort. """

        # reset the search info
        self.reset_cells_for_search()

        # choose the search structure based on the AI type
        if self.ai_type == "dfs":
            cells_to_search = Stack() # LIFO
        else:
            cells_to_search = Queue() # FIFO

        # start the search from the player's head
        # repeatedly removes a cell and checks its neighbors for food
        start = self.get_player()
        start.set_added_to_search_list()
        cells_to_search.add(start)

        while not cells_to_search.is_empty():
            current = cells_to_search.remove()

            for neighbor in self.get_neighbors(current):
                # skip cells we've already seen and cells we can't walk on
                if neighbor.on_search_list():
                    continue
                if not (neighbor.is_empty() or neighbor.is_food()):
                    continue

                neighbor.set_added_to_search_list()
                neighbor.set_search_parent(current)

                # found food: return the first step toward it
                if neighbor.is_food():
                    return self.get_first_cell_in_path(neighbor)

                cells_to_search.add(neighbor)

        # no reachable food: move to any safe neighbor if one exists
        safe = [c for c in self.get_neighbors(start) if not c.is_body()]
        if safe:
            return random.choice(safe)
        return self.get_random_neighbor(start)

    def get_first_cell_in_path(self, cell) -> Cell:
        """ Each cell remembers its parent, the cell that discovered it. 
            Once we find the food, we follow the parents backward from the food toward the duck. 
            We stop when the parent is the duck’s head. 
            That cell is the first step, so that’s what we return """

        player = self.get_player()
        while cell.get_search_parent() is not player:
            cell = cell.get_search_parent()
        return cell

    def reset_cells_for_search(self):
        """ clears all the search info for each cell """
        for row in self.board:
            for cell in row:
                cell.clear_search_info()

    def print_search_path(self):
        """ a helper method for printing the path """

        out = ""
        for row in self.board:
            for cell in row:
                out += "{}\t".format(cell.parent_string())
            out += "\n"
        return out

    def __str__(self):
        """ format the board to string form for debugging """
        
        out = ""
        for row in self.board:
            for cell in row:
                out += str(cell)
            out += "\n"
        return out

    class MoveMode(Enum):
        GOING_NORTH = auto()
        GOING_SOUTH = auto()
        GOING_EAST = auto()
        GOING_WEST = auto()
        AI_MODE = auto()
