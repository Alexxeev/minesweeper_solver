from typing import Tuple
from dd import autoref as _bdd
from field import MinesweeperField
from itertools import combinations

class Variable:
    def __init__(self, x: int, y: int, positive: bool) -> None:
        self.x = x
        self.y = y
        self.positive = positive

    def __repr__(self) -> str:
        return f'x={self.x}, y={self.y}, negated={self.positive}'

class Solver:
    '''
    A solver for given field state
    '''
    def __init__(self, field: MinesweeperField) -> None:
        self.solution: _bdd.BDD = _bdd.BDD()
        self.field: MinesweeperField = field
        self.formula = self.__init_bdd()

    def __init_bdd(self) -> _bdd.Function:
        '''
        Initialises a BDD and constructs a binary formula that represents mine placement
        '''
        for x, y in self.field.covered_cells_near_hints():
            self.solution.declare(f'x{x}_{y}')
        solution = None #sadly we cannot create empty expressions
        for x, y, mine_count in self.field.hints():
            dnf = self.__build_dnf(x, y, mine_count)
            if solution is None:
                solution = dnf
            else:
                solution = solution & dnf
        return solution

    def all_sat(self) -> dict[Tuple[int, int], bool]:
        '''
        Solves a given field state. If there is more than one solution then exception is thrown
        '''
        models = list(self.solution.pick_iter(self.formula))
        if len(models) != 1:
            raise Exception('Ambiguous mine placement')
        model = models[0]
        result: dict[Tuple[int, int], bool] = dict()
        for var_name, is_mine in model.items():
            split = var_name[1:].split(sep='_')
            x = int(split[0])
            y = int(split[1])
            result[x, y] = is_mine
        return result

    def __build_dnf(self, x: int, y: int, mine_count: int) -> _bdd.Function:
        '''
        Generates a binary formula that represents all possible mine placements for given hint
        '''
        neighbours = list(self.field.covered_neighbours(x, y))
        dnf = None
        for combination in combinations(neighbours, mine_count):
            vars = [Variable(x_comb, y_comb, True) for x_comb, y_comb in combination]
            vars_negated = [Variable(x_comb, y_comb, False) for x_comb, y_comb in neighbours if (x_comb, y_comb) not in combination]
            conj = self.__vars_conjunction(vars)
            if len(vars_negated) > 0:
                conj = conj & self.__vars_conjunction(vars_negated)
            if dnf is None:
                dnf = conj
            else:
                dnf = dnf | conj
        return dnf

    def __var_expression(self, var: Variable) -> _bdd.Function:
        '''
        Converts field coordinates to variable literal with corresponding indicies
        '''
        var_exp = f'x{var.x}_{var.y}'
        if not var.positive:
            var_exp = '~ ' + var_exp
        return self.solution.add_expr(var_exp)

    def __vars_conjunction(self, vars: list[Variable]) -> _bdd.Function:
        '''
        Generates a binary formula that is conjunction of given literals
        '''
        expression = self.__var_expression(vars[0])
        for var in vars[1:]:
            expression = expression & self.__var_expression(var)
        return expression

field = MinesweeperField(9, 9, 10)
print(field)
print(field.print_reference_field())
solver = Solver(field)
solution = solver.all_sat()