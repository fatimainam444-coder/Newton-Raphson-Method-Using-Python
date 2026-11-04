"""
Newton-Raphson Method: Root Finding and Convergence Analysis
Calculus project (Exercise 4.6) - beginner friendly version.

Libraries used:
  NumPy      - numbers and graph values
  Pandas     - iteration table
  Matplotlib - graphs
  SymPy      - symbolic derivative f'(x)
"""

import math
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")              # lets the program save graphs without opening a window
import matplotlib.pyplot as plt
import sympy as sp

# ------------------------------------------------------------------
# 1. SETTINGS (change these to try other problems)
# ------------------------------------------------------------------
FUNCTION_TEXT = "x**2 - 2"   # f(x), written in Python style (x**2 means x squared)
X0 = 2.0                     # initial guess
TOLERANCE = 1e-10            # stop when |x_new - x_old| < TOLERANCE
MAX_ITERATIONS = 50          # safety limit
DERIVATIVE_LIMIT = 1e-12     # if |f'(x)| is smaller than this, we treat it as zero


# ------------------------------------------------------------------
# 2. BUILD f(x) AND f'(x)
# ------------------------------------------------------------------
def build_functions(function_text):
    """Turn the text into Python functions for f(x) and f'(x) using SymPy."""
    x = sp.symbols("x")
    try:
        f_expr = sp.sympify(function_text, locals={"x": x})
    except (sp.SympifyError, SyntaxError) as error:
        raise ValueError(f"Could not read the function '{function_text}'.") from error
    df_expr = sp.diff(f_expr, x)                      # symbolic derivative
    f = sp.lambdify(x, f_expr, "numpy")               # fast numeric versions
    df = sp.lambdify(x, df_expr, "numpy")
    return f, df, f_expr, df_expr


# ------------------------------------------------------------------
# 3. NEWTON-RAPHSON LOOP
# ------------------------------------------------------------------
def newton_raphson(f, df, x0, tol, max_iter):
    """Return (table, root, converged, message)."""
    # Check the inputs first
    if tol <= 0 or max_iter < 1 or not math.isfinite(x0):
        raise ValueError("Tolerance must be positive, max iterations at least 1, "
                         "and the initial guess must be a finite number.")

    rows = []
    x_old = float(x0)
    converged = False
    message = "Maximum iterations reached without convergence."

    for n in range(1, max_iter + 1):
        fx = float(f(x_old))
        dfx = float(df(x_old))

        if not (math.isfinite(fx) and math.isfinite(dfx)):
            message = f"Stopped: non-finite value at iteration {n}."
            break
        if abs(dfx) < DERIVATIVE_LIMIT:
            message = f"Stopped: derivative is (almost) zero at x = {x_old}."
            break

        x_new = x_old - fx / dfx                      # Newton-Raphson formula
        error = abs(x_new - x_old)                    # size of the last step
        rows.append({"Iteration": n, "x_n": x_old, "f(x_n)": fx,
                     "f'(x_n)": dfx, "x_(n+1)": x_new, "Abs Error": error})

        if not math.isfinite(x_new):
            message = f"Stopped: non-finite value at iteration {n}."
            break
        x_old = x_new
        if error < tol:
            converged = True
            message = "Converged: step size is smaller than the tolerance."
            break

    return pd.DataFrame(rows), x_old, converged, message


# ------------------------------------------------------------------
# 4. GRAPHS
# ------------------------------------------------------------------
def make_graphs(f, table, root, x0, prefix="fig"):
    # Graph 1: the function with the root marked
    xs = np.linspace(-0.5, x0 + 0.5, 400)
    plt.figure(figsize=(7, 4.5))
    plt.plot(xs, f(xs), label="f(x) = x² − 2", color="tab:blue")
    plt.axhline(0, color="black", linewidth=0.8)
    plt.scatter([root], [0], color="red", zorder=5, label=f"Approximate root ≈ {root:.6f}")
    plt.annotate("root", xy=(root, 0), xytext=(root - 0.9, 1.2),
                 arrowprops=dict(arrowstyle="->"))
    plt.title("Graph of f(x) = x² − 2 and Its Positive Root")
    plt.xlabel("x"); plt.ylabel("f(x)")
    plt.grid(True, alpha=0.3); plt.legend()
    plt.tight_layout(); plt.savefig(f"{prefix}1_function.png", dpi=200); plt.close()

    # Graph 2: approximations against iteration number
    iters = [0] + list(table["Iteration"])
    approx = [x0] + list(table["x_(n+1)"])
    plt.figure(figsize=(7, 4.5))
    plt.plot(iters, approx, "o-", color="tab:green", label="Approximation x_n")
    plt.axhline(math.sqrt(2), color="red", linestyle="--", label="√2 (reference)")
    plt.title("Convergence of the Approximations")
    plt.xlabel("Iteration number n"); plt.ylabel("Approximation x_n")
    plt.grid(True, alpha=0.3); plt.legend()
    plt.tight_layout(); plt.savefig(f"{prefix}2_convergence.png", dpi=200); plt.close()

    # Graph 3: absolute error (log scale, zeros replaced to avoid log(0))
    err = np.array(table["Abs Error"], dtype=float)
    err_safe = np.where(err > 0, err, np.finfo(float).tiny)
    plt.figure(figsize=(7, 4.5))
    plt.semilogy(table["Iteration"], err_safe, "s-", color="tab:purple", label="|x_(n+1) − x_n|")
    plt.axhline(TOLERANCE, color="red", linestyle="--", label=f"Tolerance = {TOLERANCE:g}")
    plt.title("Error Convergence (Logarithmic Scale)")
    plt.xlabel("Iteration number n"); plt.ylabel("Absolute error")
    plt.grid(True, which="both", alpha=0.3); plt.legend()
    plt.tight_layout(); plt.savefig(f"{prefix}3_error.png", dpi=200); plt.close()


# ------------------------------------------------------------------
# 5. MAIN PROGRAM
# ------------------------------------------------------------------
def main():
    f, df, f_expr, df_expr = build_functions(FUNCTION_TEXT)
    print(f"f(x)  = {f_expr}")
    print(f"f'(x) = {df_expr}  (found by SymPy)")
    print(f"Initial guess = {X0}, tolerance = {TOLERANCE}, max iterations = {MAX_ITERATIONS}\n")

    table, root, converged, message = newton_raphson(f, df, X0, TOLERANCE, MAX_ITERATIONS)

    pd.set_option("display.float_format", lambda v: f"{v:.12g}")
    pd.set_option("display.width", 140)
    print(table.to_string(index=False))
    table.to_csv("iteration_table.csv", index=False)

    print("\n--- Final results ---")
    print(f"Approximate root : {root:.15f}")
    print(f"f(root)          : {float(f(root)):.3e}")
    print(f"Iterations used  : {len(table)}")
    print(f"Final error      : {table['Abs Error'].iloc[-1]:.3e}")
    print(f"Tolerance        : {TOLERANCE:g}")
    print(f"Converged        : {converged}  ({message})")
    print(f"True sqrt(2)     : {math.sqrt(2):.15f}")
    print(f"Actual error vs sqrt(2): {abs(root - math.sqrt(2)):.3e}")

    make_graphs(f, table, root, X0)

    # ---- Extra experiments used in the Discussion section ----
    print("\n--- Different starting guesses (same f, same tolerance) ---")
    for guess in [1.0, 1.5, 2.0, 10.0, -3.0, 100.0]:
        t, r, c, m = newton_raphson(f, df, guess, TOLERANCE, MAX_ITERATIONS)
        print(f"x0 = {guess:>6}: iterations = {len(t):>2}, root = {r:.12f}, converged = {c}")

    print("\n--- Derivative-zero test (x0 = 0) ---")
    t, r, c, m = newton_raphson(f, df, 0.0, TOLERANCE, MAX_ITERATIONS)
    print(f"Converged = {c}. Message: {m}")

    print("\n--- Invalid input test (tolerance = -1) ---")
    try:
        newton_raphson(f, df, 1.0, -1, 10)
    except ValueError as error:
        print("ValueError caught:", error)


if __name__ == "__main__":
    main()
