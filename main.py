from z3 import * # type: ignore
import time

def find_all_solutions(solver: Solver):
    solv_copy = Solver()
    solv_copy = solver.translate(solv_copy.ctx)
    solutions = []
    while solv_copy.check() == sat:
        sol = solv_copy.model()
        solutions.append(sol)
        solv_copy.add(Or([var() != sol[var] for var in sol]))
    return solutions

# Piece = DeclareSort('Piece')
# is_white = Function('is_white', Piece, BoolSort())

# p = Const('p', Piece)
# q = Const('q', Piece)

# s = Solver()
# s.add(is_white(p))
# s.add(Exists([p], is_white(p)))
# s.add(Exists([q], And(is_white(q), q != p)))
# s.add(Exists([q], And(Not(is_white(q)), q != p)))
# print(s.check())  # sat

# solutions = find_all_solutions(s)
# for sol in solutions:
#     print(sol)

n = 2
solver = Solver()
chessboard = [[]]
celllist = []
Cell = DeclareSort('Cell')
Piece = DeclareSort('Piece')
HasRow = Function('hasRow', Cell, IntSort())
HasCol = Function('hasCol', Cell, IntSort())
HasCell = Function('hasCell', Piece, Cell)
SameRow = Function('sameRow', Cell, Cell, BoolSort())
SameCol = Function('sameCol', Cell, Cell, BoolSort())

# Cell conditions
for row in range(1, n+1):
    chessboard.append([None])
    for col in range(1, n+1):
        cell = Const(f'c{row}{col}', Cell)
        chessboard[row].append(cell)
        celllist.append(cell)
        solver.add(HasRow(cell) == row)
        solver.add(HasCol(cell) == col)
c1 = Const('dumcell1', Cell)
c2 = Const('dumcell2', Cell)
solver.add(ForAll([c1], And(HasRow(c1) >= 1, HasRow(c1) <= n, HasCol(c1) >= 1, HasCol(c1) <= n)))
solver.add(ForAll([c1, c2], Implies(c1 != c2, Or(HasRow(c1) != HasRow(c2), HasCol(c1) != HasCol(c2)))))
solver.add(ForAll([c1, c2], Implies(SameRow(c1, c2), HasRow(c1) == HasRow(c2))))
solver.add(ForAll([c1, c2], Implies(SameCol(c1, c2), HasCol(c1) == HasCol(c2))))

# solutions = find_all_solutions(solver)
# for sol in solutions:
#     print(sol)

solver.check()
model = solver.model()
print(model)