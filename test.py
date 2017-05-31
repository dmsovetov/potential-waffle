from math import log, cos, sin, sqrt

from calculus import euler_approximation, newton_solver, Polynomial, fixed_point


def f0(x):
    return log(x + 1.0) + 1.0

print fixed_point(f0, 0.0)
print fixed_point(cos, 0.0)


def test_x2_euler(value, steps):
    print value, 'squared is', float(value)*value, '~', euler_approximation(0, value, steps, lambda x: x*x, lambda x: 2*x)


def test_ln_euler(value, steps):
    print value, 'ln', log(value), '~', euler_approximation(1, value, steps, log, lambda x: 1.0/x)


def test_sin_euler(value, steps):
    print value, 'sin', sin(value), '~', euler_approximation(0, value, steps, sin, lambda x: cos(x))


def test_sqrt_euler(value, steps):
    print value, 'sqrt', sin(value), '~', euler_approximation(1, value, steps, sqrt, lambda x: 1.0 / (2.0 * sqrt(x)))


#print newton_solver(-2, Polynomial(-4, -2, -2, -3))
#print newton_solver(0, Polynomial(3, -6, 4, -4, -3, -3))
#print newton_solver(-2, Polynomial(5, 0, -5, 7))
#print newton_solver(-2, Polynomial(-6, -5, 7, 1, -2, -2))
#print newton_solver(4, Polynomial(-1, 5, -4, 6, -2, 3))
#print newton_solver(0, Polynomial(-7, -6, 1, 4, 4, 2))
#print newton_solver(2, Polynomial(1, -3, -3, 6, 6, -6))
print newton_solver(-4, Polynomial(-2, -4, 5, -6))

test_x2_euler(50, 10)
test_ln_euler(20, 10)
test_sin_euler(0.5, 33)
test_sin_euler(10, 100)
