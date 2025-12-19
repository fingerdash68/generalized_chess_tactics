from z3 import * # type: ignore
import time

SOLVER_VARIABLES = []

def find_all_solutions(solver: Solver):
    solv_copy = Solver()
    solv_copy = solver.translate(solv_copy.ctx)
    solutions = []
    while solv_copy.check() == sat:
        sol = solv_copy.model()
        solutions.append(sol)
        solv_copy.add(Or([var != sol[var] for var in SOLVER_VARIABLES]))
        break
    return solutions

Piece = DeclareSort('Piece')
is_white = Function('is_white', Piece, BoolSort())

p = Const('p', Piece)
q = Const('q', Piece)

# There exists a piece that is white
s = Solver()
s.add(is_white(p))
s.add(Exists([p], is_white(p)))
s.add(Exists([q], And(is_white(q), q != p)))
s.add(Exists([q], And(Not(is_white(q)), q != p)))
print(s.check())  # sat

solutions = find_all_solutions(s)
for sol in solutions:
    print(sol)