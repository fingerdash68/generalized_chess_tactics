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

n = 3
solver = Solver()
chessboard = [[]]

# Sorts
Cell, celllist = EnumSort('Cell', [f'c{r}{c}' for r in range(1, n+1) for c in range(1, n+1)])
Piece = DeclareSort('Piece')
Color, (White, Black) = EnumSort('Color', ['White', 'Black'])
colorList = (White, Black)
PieceType, (Pawn, Knight, Bishop, Rook, Queen, King) = EnumSort('PieceType', ['Pawn', 'Knight', 'Bishop', 'Rook', 'Queen', 'King'])
typeList = {Pawn:8, Knight:2, Bishop:2, Rook:2, Queen:1, King:1}

# Cell functions
HasRow = Function('hasRow', Cell, IntSort())
HasCol = Function('hasCol', Cell, IntSort())
SameRow = Function('sameRow', Cell, Cell, BoolSort())
SameCol = Function('sameCol', Cell, Cell, BoolSort())
SameLine = Function('sameLine', Cell, Cell, BoolSort())
SameForDiag = Function('sameForDiag', Cell, Cell, BoolSort())
SameBackDiag = Function('sameBackDiag', Cell, Cell, BoolSort())
SameDiag = Function('sameDiag', Cell, Cell, BoolSort())
CellHasColor = Function('cellHasColor', Cell, Color)
CanSeeBottom = Function('canSeeBottom', Cell, Cell, BoolSort())
CanSeeTop = Function('canSeeTop', Cell, Cell, BoolSort())
CanSeeLeft = Function('canSeeLeft', Cell, Cell, BoolSort())
CanSeeRight = Function('canSeeRight', Cell, Cell, BoolSort())
CanSeeBottomRight = Function('canSeeBottomRight', Cell, Cell, BoolSort())
CanSeeBottomLeft = Function('canSeeBottomLeft', Cell, Cell, BoolSort())
CanSeeTopRight = Function('canSeeTopRight', Cell, Cell, BoolSort())
CanSeeTopLeft = Function('canSeeTopLeft', Cell, Cell, BoolSort())
HasPiece = Function('hasPiece', Cell, BoolSort())

# Piece functions
HasType = Function('hasType', Piece, PieceType)
PieceHasColor = Function('pieceHasColor', Piece, Color)
OnCell = Function('onCell', Piece, Cell)
CanMoveTo = Function('canMoveTo', Piece, Cell, BoolSort())

# Cell conditions
for row in range(1, n+1):
    chessboard.append([None])
    for col in range(1, n+1):
        cell = celllist[(row-1) * n + col-1]
        chessboard[row].append(cell)
        solver.add(HasRow(cell) == row)
        solver.add(HasCol(cell) == col)
        if (row + col)%2 == 0:
            solver.add(CellHasColor(cell) == Black)
        else:
            solver.add(CellHasColor(cell) == White)
c1 = Const('dumcell1', Cell)
c2 = Const('dumcell2', Cell)
c3 = Const('dumcell3', Cell)
# solver.add(ForAll([c1], And(HasRow(c1) >= 1, HasRow(c1) <= n, HasCol(c1) >= 1, HasCol(c1) <= n)))
# solver.add(ForAll([c1, c2], Implies(c1 != c2, Or(HasRow(c1) != HasRow(c2), HasCol(c1) != HasCol(c2)))))
solver.add(ForAll([c1, c2], SameRow(c1, c2) == (HasRow(c1) == HasRow(c2))))
solver.add(ForAll([c1, c2], SameCol(c1, c2) == (HasCol(c1) == HasCol(c2))))
solver.add(ForAll([c1, c2], SameLine(c1, c2) == Or(SameRow(c1, c2), SameCol(c1, c2))))
solver.add(ForAll([c1, c2], SameForDiag(c1, c2) == (HasRow(c2) - HasRow(c1) == HasCol(c2) - HasCol(c1))))
solver.add(ForAll([c1, c2], SameBackDiag(c1, c2) == (HasRow(c2) - HasRow(c1) == HasCol(c1) - HasCol(c2))))
solver.add(ForAll([c1, c2], SameDiag(c1, c2) == Or(SameForDiag(c1, c2), SameBackDiag(c1, c2))))

# Piece conditions
p1 = Const('dumpiece1', Piece)
p2 = Const('dumpiece2', Piece)
solver.add(ForAll([p1, p2], Implies(p1 != p2, OnCell(p1) != OnCell(p2))))
solver.add(ForAll([c1], Exists([p1], OnCell(p1) == c1) == (HasPiece(c1))))
for ty, nb in typeList.items():
    dumlist = [Const(f'dum{i}', Piece) for i in range(nb+1)]
    dumcolor = Const('dumcolor', Color)
    andcond = And([And(HasType(dum) == ty, PieceHasColor(dum) == dumcolor) for dum in dumlist])
    solver.add(ForAll([dumcolor] + dumlist, Implies(andcond, Not(Distinct(dumlist)))))

# Piece-cell conditions
solver.add(ForAll([c1, c2, c3], CanSeeBottom(c1, c2) == And(SameCol(c1, c2), HasRow(c2) < HasRow(c1), Implies(And(SameCol(c1, c3), HasRow(c3) < HasRow(c1), HasRow(c3) > HasRow(c2)), Not(HasPiece(c3))))))

solver.add(ForAll([p1], Or(OnCell(p1) == chessboard[1][1], OnCell(p1) == chessboard[1][2])))
solver.add(OnCell(p1) == chessboard[1][1])
solver.add(OnCell(p2) == chessboard[1][2])

# solutions = find_all_solutions(solver)
# for sol in solutions:
#     print(sol)

start = time.time()

if solver.check() == sat:
    model = solver.model()
    print(model)
    for i in range(1, n+1):
        for j in range(1, n+1):
            print(f"{i}, {j} : ", model.eval(CanSeeBottom(chessboard[n][1], chessboard[i][j])))
else:
    print("unsatisfiable")

print("temps :", time.time() - start)