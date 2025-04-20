from math import isqrt

def solve_pells_equation(D):
    
    if isqrt(D) ** 2 == D:
        raise ValueError("D must not be a perfect square")

    # Continued fraction expansion of sqrt(D)
    m = 0
    d = 1
    a = a0 = isqrt(D)
    x_prev, x_curr = 1, a0
    y_prev, y_curr = 0, 1

    while x_curr ** 2 - D * y_curr ** 2 != 1:
        m = d * a - m
        d = (D - m ** 2) // d
        a = (a0 + m) // d
        x_next = a * x_curr + x_prev
        y_next = a * y_curr + y_prev
        x_prev, x_curr = x_curr, x_next
        y_prev, y_curr = y_curr, y_next

    return x_curr, y_curr
