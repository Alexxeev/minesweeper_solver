from solver import FieldSolver
from field import Field

if __name__ == '__main__':
    print('''
    Choose a field to be solved:
    1. Beginner — 9x9, 10 mines
    2. Intermidiate - 16x16, 32 mines
    3. Expert - 30x16, 99 mines
    ''')
    choice = input('Choice: ')
    field = None
    match choice:
        case '1':
            field = Field(9, 9, 10)
        case '2':
            field = Field(16, 16, 32)
        case '3':
            field = Field(30, 16, 99)
        case _:
            print('Errorneus field selection')
            exit()
    solver = FieldSolver(field)
    for step in solver.solve():
        print(step)