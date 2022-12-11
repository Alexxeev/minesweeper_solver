from typing import Generator, Tuple
import numpy as np
import random as rand

class MinesweeperField:
    def __init__(self, length: int, height: int, number_of_mines: int) -> None:
        self.length: int = length
        self.height: int = height
        self.reference_grid: np.ndarray = np.zeros((length, height), dtype=np.int64)
        self.game_grid: np.ndarray = np.full((length, height), dtype=np.str_, fill_value='*')
        self.number_of_mines: int = number_of_mines
        self.__fill_random()
        self.__init_state()
    
    def __repr__(self) -> str:
        return self.game_grid.__str__()

    def __init_state(self):
        x, y = self.__choose_random_empty_cell()
        self.open_up(x, y)

    def print_reference_field(self) -> str:
        return self.reference_grid
    
    def __choose_random_empty_cell(self) -> Tuple[int, int]:
        x, y = 0, 0
        while self.reference_grid[x,y] != 0:
            x, y = np.random.randint(self.length), np.random.randint(self.height)
        return x, y
    
    def __uncover_field(self, x: int, y: int):
        match self.reference_grid[x,y]:
            case 0:
                self.game_grid[x,y] = ' '
            case -1:
                self.game_grid[x,y] = 'X'
            case _:
                self.game_grid[x,y] = str(self.reference_grid[x,y])
    
    def neighbours(self, x: int, y: int) -> Generator:
        if x > 0 and y > 0:
            yield x - 1, y - 1
        if y > 0:
            yield x, y - 1
        if x < self.length - 1 and y > 0:
            yield x + 1, y - 1
        if x > 0:
            yield x - 1, y
        if x < self.length - 1:
            yield x + 1, y
        if x > 0 and y < self.height - 1:
            yield x - 1, y + 1
        if y < self.height - 1:
            yield x, y + 1
        if x < self.length - 1 and y < self.height - 1:
            yield x + 1, y + 1

    def covered_neighbours(self, x: int, y: int) -> Generator:
        for x_neighbour, y_neighbour in self.neighbours(x, y):
            if self.game_grid[x_neighbour, y_neighbour] == '*':
                yield x_neighbour, y_neighbour
    
    def covered_cells_near_hints(self) -> Generator:
        for x in range(0, self.length):
            for y in range(0, self.height):
                if self.game_grid[x, y] == '*' and self.__is_hint_nearby(x, y):
                    yield x, y
    
    def open_up(self, x: int, y: int):
        if self.game_grid[x,y] == '*':
            self.__uncover_field(x,y)
            if self.reference_grid[x,y] == 0:
                for x_neigbour, y_neighbour in self.neighbours(x,y):
                    self.open_up(x_neigbour, y_neighbour)
        return self
    
    def hints(self) -> Generator:
        for x in range(0, self.length):
            for y in range(0, self.height):
                if self.game_grid[x, y] > '0' and self.game_grid[x,y] < '9':
                    yield x, y, self.reference_grid[x,y]

    def __fill_random(self):
        return self.__place_mines().__place_hints()

    def __place_mines(self):
        number_placed = 0
        while number_placed < self.number_of_mines:
            x, y = rand.randint(0, self.length - 1), rand.randint(0, self.height - 1)
            if (self.reference_grid[x, y] != -1):
                self.reference_grid[x, y] = -1
                number_placed += 1
        return self

    def __is_hint_nearby(self, x: int, y: int) -> bool:
        for x_neigbour, y_neighbour in self.neighbours(x, y):
            if self.reference_grid[x_neigbour, y_neighbour] in range(1, 9) and self.game_grid[x_neigbour, y_neighbour] != '*':
                return True
        return False

    def __is_mine(self, x: int, y: int) -> int:
        if x >= 0 and x < self.length and y >= 0 and y < self.height and self.reference_grid[x, y] == -1:
            return 1
        return 0

    def __mines_near_count(self, x: int, y: int) -> int:
        count_near = 0
        for x_neighbour, y_neighbour in self.neighbours(x, y):
            count_near += self.__is_mine(x_neighbour, y_neighbour)
        return count_near
    
    def __place_hints(self):
        for x in range(0, self.length):
            for y in range(0, self.height):
                if not self.__is_mine(x, y):
                    self.reference_grid[x, y] = self.__mines_near_count(x, y)
        return self
    


# field = MinesweeperField(9, 9, 10)
# print(field)
# for unc in field.covered_cells_near_hints():
#     print(unc)