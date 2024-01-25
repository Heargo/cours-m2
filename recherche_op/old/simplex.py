import numpy as np


def simplex_algorithm(c, A, b):
    m, n = A.shape
    tableau = np.zeros((m + 1, n + m + 1))

    # Initialize tableau
    tableau[:-1, :n] = A
    tableau[:-1, -1] = b
    tableau[-1, :n] = -c
    tableau[-1, -1] = 0

    while any(tableau[-1, :n] < 0):
        # Choose entering variable (column k with the most negative coefficient)
        entering_var = np.argmin(tableau[-1, :n])

        # Choose leaving variable (row l with the minimum ratio b[i]/A[i, k] where A[i, k] > 0)
        ratios = tableau[:-1, -1] / tableau[:-1, entering_var]
        leaving_var = np.argmin(ratios)

        # Update the tableau
        pivot = tableau[leaving_var, entering_var]
        tableau[leaving_var, :] /= pivot
        for i in range(m + 1):
            if i != leaving_var:
                tableau[i, :] -= tableau[i, entering_var] * \
                    tableau[leaving_var, :]

    # Extract optimal solution and objective value
    solution = tableau[:-1, -1]
    objective_value = -tableau[-1, -1]

    return solution, objective_value


# Test the implementation with the provided example
c = np.array([30, 50, 0, 0, 0, 0])
A = np.array([[3, 2, 1, 0, 0, 0],
              [1, 0, 0, 1, 0, 0],
              [0, 1, 0, 0, 1, 0]])
b = np.array([1800, 400, 600])

solution, objective_value = simplex_algorithm(c, A, b)

print("Optimal Solution:", solution)
print("Optimal Objective Value:", objective_value)
