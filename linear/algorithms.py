from matrix import Matrix
from vector import Vector


def is_close(a, b, rel_tol=1e-09, abs_tol=1e-09):
    """ Returns true if a floating point value lies near the specified value """
    return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)


def transposed(matrix):
    """ Returns a transpose of this matrix """

    result = Matrix(matrix.cols, matrix.rows)

    for i in range(0, result.rows):
        result[i] = matrix.column(i)

    return result


def column_space(matrix):
    """ Returns a column space for a given matrix """

    r_ref, pivots, free_columns = gauss_elimination(matrix)

    vectors = []
    for row, column in pivots:
        vectors.append(matrix.column(column).items)

    return transposed(Matrix.from_rows(vectors))


def null_space(matrix):
    """ Returns a null space of an input matrix """

    # Perform Gauss elimination
    r_ref, pivots, free_columns = gauss_elimination(matrix)

    result = Matrix(matrix.cols, len(free_columns))

    for pivot_row, pivot_column in pivots:
        for j, free in enumerate(free_columns):
            result[pivot_column][j] = -matrix[pivot_row][free]

    for i, column in enumerate(free_columns):
        result[column][i] = 1.0

    return result


def gauss_elimination(matrix):
    """ Takes an input matrix and returns it in reduced row echelon form """

    # Make a deep copy of an input matrix
    r_ref = matrix.copy()

    # Convert to a reduced row echelon form
    pivots, free = inplace_gauss_elimination(r_ref)

    return r_ref, pivots, free


def det(matrix):
    """ Calculates a determinant of an input matrix """

    triangular, sign = upper_triangular(matrix)
    result = 1.0

    for i in range(0, triangular.diagonal_size):
        result *= triangular[i][i]

    return result * sign


def upper_triangular(matrix):
    """ Returns an upper triangular for of an input matrix """

    # Make a deep copy of an input matrix
    return inplace_upper_triangular(matrix.copy())


def inplace_upper_triangular(matrix):
    """ Converts an input matrix to a upper triangular one by running Gauss elimination on it """

    sign = 1.0

    for step in range(0, matrix.diagonal_size):
        coefficient = matrix[step][step]

        if is_close(coefficient, 0.0):
            for i in range(step, matrix.diagonal_size):
                if matrix[i][step] != 0.0:
                    matrix.swap_rows(step, i)
                    sign *= -1
                    break

            coefficient = matrix[step][step]

        if is_close(coefficient, 0.0):
            continue

        for idx in range(step + 1, matrix.rows):
            matrix[idx] -= matrix[step] * (matrix[idx][step] / coefficient)

    return matrix, sign


def inplace_gauss_elimination(r_ref):
    """ Converts the input matrix to a reduced row echelon form """

    # Perform a first pass of Gauss elimination process

    for step in range(0, r_ref.diagonal_size):
        r_ref.sort_rows(lambda matrix_row: -abs(matrix_row[step]), start_from=step)

        coefficient = r_ref[step][step]

        if is_close(coefficient, 0.0):
            continue

        for idx in range(step + 1, r_ref.rows):
            r_ref[idx] -= r_ref[step] * (r_ref[idx][step] / coefficient)

    # Convert all values that are near the zero to zero
    r_ref.zero_small_values()

    # Get the pivot and free entries
    pivots = [(i, row.pivot_index) for i, row in enumerate(r_ref) if row.pivot_index is not None]
    free = [i for i in range(0, r_ref.cols) if i not in [i for i, c in pivots]]

    # Now convert a row echelon matrix to a reduced row echelon form

    for pivot_row, pivot_column in pivots:
        for row in range(pivot_row - 1, -1, -1):
            r_ref[row] -= r_ref[pivot_row] * (r_ref[row][pivot_column] / r_ref[pivot_row][pivot_column])

    # Finally, normalize each row by a leading coefficient

    for i, row in enumerate(r_ref):
        leading = None

        for j in range(i, r_ref.cols):
            if row[j] != 0:
                leading = row[j]
                break

        if leading is None:
            break

        r_ref[i] /= leading

    return pivots, free


def linear_combination(basis, scalars):
    """ Calculates a linear combination of input vectors """

    assert len(basis) > 0
    assert len(basis) == len(scalars)

    for e in basis:
        assert isinstance(e, Vector)

    # Create an instance of a resulting vector
    result = Vector([0.0] * basis[0].dim)

    # Combine basis vectors
    for i, s in enumerate(scalars):
        result += basis[i] * s

    return result


def bilinear(matrix, a, b):
    """ Calculates a bilinear form value for two given vectors """

    result = Matrix.from_row_vectors([a]) * matrix * Matrix.from_column_vectors([b])

    return result[0][0]


def quadratic(matrix, vector):
    """ Calculates a quadratic form value for a given vector """

    result = Matrix.from_row_vectors([vector]) * matrix * Matrix.from_column_vectors([vector])

    return result[0][0]


def is_orthagonal(basis):
    """ Checks that a set of vectors is orthagonal """

    for i, v1 in enumerate(basis):
        for j, v2 in enumerate(basis):
            if i == j:
                continue

            if not is_close(v1 * v2,  0.0):
                return False

    return True


def is_basis(vectors):
    """ Returns true if a given set of vectors is linearly independent """

    c = column_space(Matrix.from_columns([v.items for v in vectors]))
    return c.dimensions[1] == len(vectors)


def gram_schmidt(basis, normalize=True):
    """ Performs a Gram-Schmidt orthogonalization process on a set of vectors """

    assert is_basis(basis)

    result = []

    for i in range(0, len(basis)):
        e = basis[i]

        # Calculate scalars for each existing basis vector
        s = [-v.project(e)[1] for v in result]

        # Next basis vector is a linear combination of previously calculated
        n = linear_combination([e] + result, [1.0] + s)

        result.append(n)

    if normalize:
        result = [n.normalized() for n in result]

    assert is_orthagonal(result)

    return result
