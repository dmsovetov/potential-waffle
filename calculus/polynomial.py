from linear import Matrix
from linear import Vector


class Polynomial(object):
    def __init__(self, *args):
        """ Constructs a n-th power polynomial instance """

        if len(args) == 1 and isinstance(args[0], Vector):
            args = args[0].items

        non_zero = next((i for i, x in enumerate(args) if x), None)
        args = args[non_zero:]

        self._coefficients = Vector(args)
        self._d_dx = self.d_dx

    def __repr__(self):
        """ Converts a polynomial to a string value """

        def monomial(idx, coefficient):
            return (str(coefficient) if coefficient != 1.0 else '') +\
                   ('x^' + str(self.power - idx) if idx != self.power else '')

        return ' + '.join([monomial(i, k) for i, k in enumerate(self._coefficients)])

    def __call__(self, *args, **kwargs):
        """ Evaluates value for a given input """

        value = 0.0

        for i, v in enumerate(self._coefficients):
            value += v * pow(args[0], self.power - i)

        return value

    @property
    def derivative(self):
        """ Computes the derivative for this polynomial """

        return Polynomial(self._d_dx * self._coefficients)

    @property
    def power(self):
        """ Returns a polynomial power """

        return self._coefficients.dim - 1

    @property
    def d_dx(self):
        n = self.power + 1
        operator = Matrix(n, n)
        v = 1.0

        for i in range(n - 1, 0, -1):
            operator[i][i - 1] = v
            v += 1.0

        return operator

