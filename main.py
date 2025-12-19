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

# solver = Solver()
# bk_file = Int('bk_file')
# bk_rank = Int('bk_rank')
# SOLVER_VARIABLES.extend([bk_file, bk_rank])
# solver.add(And(bk_rank >= 0, bk_rank <= 7))
# # solver.add(bk_rank == 7)
# solver.add(And(bk_file >= 0, bk_file <= 7))

Piece = DeclareSort('Piece')
is_white = Function('is_white', Piece, BoolSort())

p = Const('p', Piece)

# There exists a piece that is white
s = Solver()
s.add(Exists([p], is_white(p)))
print(s.check())  # sat

solutions = find_all_solutions(s)
for sol in solutions:
    print(sol)