import timeit
from solvers import RecursiveSolver

for i in range(4, 13):
    solver = RecursiveSolver(i)
    solutions = solver.search_n_queens()
    exec_time = timeit.timeit(lambda: solver.search_n_queens(), number=1)
    print(f"N: {i}")
    print(f"Number of solutions: {len(solutions)}")
    print(f"Execution time: {exec_time}\n\n")
