from matrix import Matrix
from vector import Vector
from algorithms import inplace_gauss_elimination, column_space, null_space, det, linear_combination, gram_schmidt, bilinear, quadratic


class RRef(Matrix):
    """ Matrix in a reduced row echelon form """

    def __init__(self, matrix):
        """ Constructs a reduced row echelon form matrix from a given input """

        assert isinstance(matrix, Matrix)

        Matrix.__init__(self, matrix.rows, matrix.cols)
        self.set(matrix)
        self._pivots = inplace_gauss_elimination(self)

        self._original = matrix
        self._pivot_columns = [column for row, column in self._pivots]
        self._free_columns = [i for i in range(0, matrix.cols) if i not in self._pivot_columns]

    @property
    def null_space(self):
        """ Returns a null space as a matrix """

        result = Matrix(self.cols, len(self.free_columns))

        for pivot_row, pivot_column in self._pivots:
            for j, free in enumerate(self.free_columns):
                result[pivot_column][j] = -self[pivot_row][free]

        for i, column in enumerate(self.free_columns):
            result[column][i] = 1.0

        return result

    @property
    def rank(self):
        """ Returns a rank of a matrix """

        return len(self.pivot_columns)

    @property
    def original(self):
        """ Returns the original matrix """

        return self._original

    @property
    def pivot_columns(self):
        """ Returns a list of indices of pivot columns """

        return self._pivot_columns

    @property
    def free_columns(self):
        """ Returns a list of indices of free columns """

        return self._free_columns

print det(Matrix.from_rows([
    [0, 0, 3, 1],
    [-4, 2, 4, 1],
    [0, 2, 1, -2],
    [2, 1, 0, -2]
]))


'''print RRef(Matrix.from_rows([
    [1, 1, 1, 1],
    [1, 2, 3, 4],
    [4, 3, 2, 1]
]))

print

print RRef(Matrix.from_rows([
    [1, 1, 1, 1],
    [2, 1, 4, 3],
    [3, 4, 1, 2]
]))

print

print RRef(Matrix.from_rows([
    [1, 1, 2, 3, 2],
    [1, 1, 3, 1, 4]
]))'''

A = Matrix.from_rows([
    [2, 1, 7, -7, 2],
    [-3, 4, -5, -6, 3],
    [1, 1, 4, -5, 2]
])

print 'Column space of A:'
print column_space(A)
print 'Null space of A:'
print null_space(A)

'''print RRef(Matrix.from_rows([
    [2, 1, 7, -7, 2],
    [-3, 4, -5, -6, 3],
    [1, 1, 4, -5, 2]
])).null_space'''

'''matrices = [
    [
        [2, 3, 1, 8],
        [4, 7, 5, 20],
        [0, -2, 2, 0]
    ],
    [
        [2, 1, 0, 0, 0],
        [1, 2, 1, 0, 0],
        [0, 1, 2, 1, 0],
        [0, 0, 1, 2, 5]
    ],
    [
        [4, 2, 8],
        [5, 2, 4],
        [2, 6, 2],
        [3, 0, 8]
    ],
    [
        [1, 2, 5],
        [1, 3, 4]
    ],
    [
        [1, -1, 4],
        [1, 0, 5],
        [1, 1, 9]
    ],
    [
        [2, -1, 2],
        [1, 2, 1],
        [1, 1, 4]
    ],
    [
        [2, -2, -1],
        [-2, 2, 7],
        [5, 3, -26]
    ],
    [
        [1, 1, 2, 1],
        [1, 1, 2, 3]
    ],
    [
        [1, 1, 1]
    ]
]


for i in range(0, len(matrices)):
    m = Matrix.from_values(matrices[i])
    r = RRef(m)

    for j, row in enumerate(m):
        print row, '\t', r[j]
    print'''

print 'Linear combination: ', linear_combination([Vector(1.0, 0.0), Vector(0.0, 1.0)], [5.0, -2.0])

print 'Ortho basis:\n', Matrix.from_column_vectors(gram_schmidt([
    Vector(1, 2, -3),
    Vector(1, 0, -5),
    Vector(-2, 1, 1)
], normalize=False))

print 'Bilinear form: ', bilinear(Matrix.from_columns([
    [1, 0],
    [0, 1]
]), Vector(2, 2), Vector(3, 3))

print 'Quadratic form: ', quadratic(Matrix.from_columns([
    [1, 0],
    [0, 1]
]), Vector(2, 2))
