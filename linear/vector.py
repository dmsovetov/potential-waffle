from math import sqrt


class Vector(object):
    def __init__(self, *args):
        """ Constructs a new Vector instance from input values """

        n = len(args)

        if n == 1 and isinstance(args[0], (list, tuple)):
            args = args[0]

        self._items = [float(v) for v in args]

    def __eq__(self, other):
        """ Tests the self and other for an equality """

        return self.items == other.items

    def __mul__(self, other):
        """ Multiplies a vector by a scalar or computes the dot product of two vectors """

        if isinstance(other, Vector):
            return sum(a * b for a, b in zip(self, other))
        elif isinstance(other, (int, float)):
            return self.__rmul__(other)

    def __rmul__(self, other):
        """ Multiplies a vector by a scalar value """

        assert isinstance(other, (int, float))

        product = tuple(a * other for a in self)
        return Vector(*product)

    def __div__(self, other):
        """ Divides a vector by a scalar value """

        assert other != 0.0
        return self.__rmul__(1.0 / other)

    def __add__(self, other):
        """ Returns the vector addition of self and other """

        added = tuple(a + b for a, b in zip(self, other))
        return Vector(*added)

    def __sub__(self, other):
        """ Returns the vector difference of self and other """

        subbed = tuple(a - b for a, b in zip(self, other))
        return Vector(*subbed)

    def __setitem__(self, index, value):
        """ Sets a vector scalar value at specified index """

        assert index >= 0
        assert index < self.dim
        self.items[index] = value

    def __getitem__(self, index):
        """ Returns a vector scalar value at specified index """

        assert index >= 0
        assert index < self.dim
        return self.items[index]

    def __repr__(self):
        """ Converts a vector to a string value """

        return str(self.items)

    def __iter__(self):
        """ Returns a vector value iterator """

        return self.items.__iter__()

    def project(self, other):
        """ Projects other vector onto this one and returns a projection and it's length """

        alpha = (self * other) / (self * self)
        return self * alpha, alpha

    def normalized(self):
        """ Returns a normalized vector """

        return (1.0 / self.length) * self

    def copy(self):
        """ Returns a copy of this vector """

        return Vector(self.items)

    def append(self, value):
        """ Appends a new value to this vector with an increase of vector's dimensionality """

        self._items.append(float(value))

    @property
    def dim(self):
        """ Returns a vector dimensions """

        return len(self.items)

    @property
    def items(self):
        """ Returns the vector elements """

        return self._items

    @property
    def length(self):
        """ Returns the vector length """

        return sqrt(self.__mul__(self))

    @property
    def pivot_index(self):
        """ Returns an index of a pivot element """

        return next((i for i, value in enumerate(self) if value), None)


assert Vector(1).dim == 1
assert Vector(1, 2).dim == 2
assert Vector([2, 2, 3]).dim == 3
assert Vector((1, 12)).dim == 2

assert Vector(1, 2) == Vector([1, 2])

assert Vector(1, 2)*2 == Vector(2, 4)
assert Vector(1, 2)*Vector(3, 4) == 11

assert 3*Vector(1, 1) == Vector(3, 3)

assert Vector(4, 3).length == 5

assert Vector(4, 3).normalized().length == 1.0
