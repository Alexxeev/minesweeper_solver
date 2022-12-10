import numpy as np
import random as rand

class MinesweeperField:
    def __init__(self, length: int, height: int, number_of_mines: int) -> None:
        self.length: int = length
        self.height: int = height
        self.grid: np.ndarray = np.zeros((length, height), dtype=np.int64)
        self.number_of_mines: int = number_of_mines
    
    def __repr__(self) -> str:
        return f'''
length: {self.length}, height: {self.height}
{self.grid}
        '''
    
    def fill_random(self):
        return self.__place_mines().__place_hints()

    def __place_mines(self):
        number_placed = 0
        while number_placed < self.number_of_mines:
            x, y = rand.randint(0, self.length - 1), rand.randint(0, self.height - 1)
            if (self.grid[x, y] != -1):
                self.grid[x, y] = -1
                number_placed += 1
        return self

    def __is_mine(self, x: int, y: int) -> int:
        if x >= 0 and x < self.length and y >= 0 and y < self.height and self.grid[x, y] == -1:
            return 1
        return 0

    def __mines_near(self, x: int, y: int) -> int:
        count_near = 0
        count_near += self.__is_mine(x - 1, y - 1)
        count_near += self.__is_mine(x, y - 1)
        count_near += self.__is_mine(x + 1, y - 1)
        count_near += self.__is_mine(x - 1, y)
        count_near += self.__is_mine(x + 1, y)
        count_near += self.__is_mine(x - 1, y + 1)
        count_near += self.__is_mine(x, y + 1)
        count_near += self.__is_mine(x + 1, y + 1)
        return count_near
    
    def __place_hints(self):
        for x in range(0, self.length):
            for y in range(0, self.height):
                if not self.__is_mine(x, y):
                    self.grid[x, y] = self.__mines_near(x, y)
        return self


field = MinesweeperField(9, 9, 10).fill_random()
print(field)
