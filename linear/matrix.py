from vector import Vector


class MatrixError(Exception):
    """ An exception class for Matrix """
    pass


class Matrix(object):
    def __init__(self, rows, cols):
        """ Constructs an instance of a Matrix class as a list of row vectors"""

        self._items = [Vector([0] * cols) for x in range(rows)]
        self._rows = rows
        self._cols = cols

    def __repr__(self):
        """ Converts a matrix to a string value """

        return '\n'.join([repr(row) for row in self._items])

    def __setitem__(self, index, value):
        """ Sets a matrix row at specified index """

        assert index >= 0
        assert index < self.rows

        if not isinstance(value, Vector):
            value = Vector(value)

        if value.dim != self.cols:
            raise MatrixError("Matrix and vector dimensions do not match")

        self.items[index] = value

    def __getitem__(self, index):
        """ Returns a matrix row at specified index """

        assert index >= 0
        assert index < self.rows
        return self.items[index]

    def __iter__(self):
        """ Returns a matrix rows iterator """

        return self.items.__iter__()

    def __mul__(self, other):
        """ Multiplies matrix with other matrix """

        if isinstance(other, Vector):
            assert other.dim == self.cols
            result = Vector()

            for i in xrange(self.cols):
                result.append(self[i] * other)

            return result

        assert isinstance(other, Matrix)

        if self.cols != other.rows:
            raise MatrixError("Matrix dimensions does not match")

        result = Matrix(self.rows, other.cols)

        for i in range(0, result.rows):
            for j in range(0, result.cols):
                result[i][j] = self[i] * other.column(j)

        return result

    def set(self, other):
        """ Copies values from an input matrix """

        assert other.dimensions == self.dimensions
        for i, row in enumerate(other):
            self._items[i] = row

    def copy(self):
        """ Returns a copy of this matrix """

        return Matrix.from_rows([v.items for v in self.items])

    def sort_rows(self, predicate, start_from=0):
        """ Sorts the matrix rows with a predicate """

        self._items[start_from:] = sorted(self._items[start_from:], key=predicate)

    def swap_rows(self, a, b):
        """ Swaps two rows by their indices """

        temp = self._items[a]
        self._items[a] = self._items[b]
        self._items[b] = temp

    def column(self, index):
        """ Returns a column vector at specified index """

        assert index >= 0
        assert index < self.cols

        return Vector([row[index] for row in self])

    def zero_small_values(self, tolerance=1e-09):
        """ Converts all values that are near the zero to zero """

        for r in self:
            for i, v in enumerate(r):
                if abs(v) < tolerance:
                    r[i] = 0

    def for_each(self, predicate, row_indices=None):
        """ Invokes a predicate for each row of a matrix """

        if row_indices is None:
            row_indices = [i for i in range(0, self.rows)]

        for idx in row_indices:
            predicate(self[idx])

    def append_row(self, row):
        """ Appends a new row to this matrix """

        assert isinstance(row, Vector)

        if row.dim != self.cols:
            raise MatrixError("Wrong row size")

        self._items.append(row)
        self._rows += 1

    def append_column(self, column):
        """ Appends a new column to this matrix """

        assert isinstance(column, Vector)

        if column.dim != self.rows:
            raise MatrixError("Wrong column size: " + str(self.rows) + " expected, got " + str(column.dim))

        for i, v in enumerate(column):
            self._items[i].append(v)

        self._cols += 1

    @property
    def items(self):
        """ Returns a collection of matrix rows """

        return self._items

    @property
    def rows(self):
        """ Returns a total number of rows in this matrix """

        return self._rows

    @property
    def cols(self):
        """ Returns a total number of columns in this matrix """

        return self._cols

    @property
    def dimensions(self):
        """ Returns the matrix dimensions as a tuple """

        return self.rows, self.cols

    @property
    def diagonal_size(self):
        """ Returns a matrix diagonal size """

        return min(self.rows, self.cols)

    @classmethod
    def read_from_input(cls):
        """ Reads a matrix from the input """

        nm = list(map(int, input().split()))

        result = []
        for i in range(0, nm[0]):
            result.append(list(map(int, input().split())))

        return Matrix.from_values(result)

    @classmethod
    def read_square_from_input(cls):
        """ Reads a matrix from the input """

        nm = list(map(int, input().split()))

        result = []
        for i in range(0, nm[0]):
            result.append(list(map(int, input().split())))

        return Matrix.from_values(result)

    @classmethod
    def identity(cls, dimensions):
        """ Constructs the identity matrix """

        result = Matrix(dimensions, dimensions)
        for i, row in enumerate(result):
            row[i] = 1

        return result

    @classmethod
    def from_rows(cls, rows):
        """ Constructs a matrix from a list of rows """

        return Matrix.from_row_vectors([Vector(v) for v in rows])

    @classmethod
    def from_row_vectors(cls, rows):
        """ Constructs a matrix from a list of row vectors """

        assert len(rows) > 0

        result = Matrix(0, rows[0].dim)
        for row in rows:
            result.append_row(row)

        return result

    @classmethod
    def from_columns(cls, columns):
        """ Constructs a matrix from a list of columns """

        return Matrix.from_column_vectors([Vector(v) for v in columns])

    @classmethod
    def from_column_vectors(cls, columns):
        """ Constructs a matrix from a list of column vectors """

        assert len(columns) > 0

        result = Matrix(columns[0].dim, 0)
        for column in columns:
            result.append_column(column)

        return result

assert Matrix(4, 3).dimensions == (4, 3)

m = Matrix(3, 3)
m[0] = Vector(1, 2, 3)
assert m[0] == Vector(1, 2, 3)

#print Matrix.from_values([[1, 2], [3, 4]]) * Matrix.from_values([[5, 6], [7, 8]])

