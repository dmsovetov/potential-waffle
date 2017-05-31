import gauss
import vector
import matrix

#A = gauss.read_matrix()
A = [
    [4, 2, 8],
    [5, 2, 4],
    [2, 6, 2],
    [3, 0, 8]
]


def solve(input_system):
    columns = matrix.columns(input_system)

    f = columns[-1]
    subspace = columns[:-1]

    system = []

    for i, e in enumerate(subspace):
        assert len(f) == len(e)

        equation = []

        for j, s in enumerate(subspace):
            equation.append(vector.dot(e, s))

        equation.append(vector.dot(e, f))

        system.append(equation)

    gauss.solve(system)

print solve(A)
