from polynomial import Polynomial


def odd(n):
    """ Computes the n-th odd number"""

    return 2*n + 1


def fixed_point(f, initial, eps=1e-10):
    """ Computes a fixed point of a function """

    y = f(initial)

    while True:
        e = f(y) - y

        if abs(e) < eps:
            break

        y += e

    return y


def euler_approximation(initial, value, steps, f, df_dx):
    """ Computes the function value for a given input by an Euler's approximation method """

    result = 0
    dx = float(value - initial) / steps

    for i in range(0, steps):
        result += df_dx(initial + dx*odd(i) * 0.5)

    return f(initial) + dx * result


def newton_solver(x0, f, eps=1e-10):
    """ Solves a polynomial by a Newton's method """

    assert isinstance(f, Polynomial)

    x = x0
    y = f(x)
    df_dx = f.derivative
    result = [x0]

    while abs(y) > eps:
        x -= y / df_dx(x)
        y = f(x)
        result.append(x)

    return result
