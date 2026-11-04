# Newton–Raphson Method Using Python

A small Python project that finds the root of an equation using the **Newton–Raphson method**. It shows every step in a table and draws graphs so you can see how the answer gets closer and closer to the real root.

This project was made for a Calculus course (Exercise 4.6, 14th edition).

---

## What is the Newton–Raphson method?

Some equations are hard to solve with simple algebra. The Newton–Raphson method finds an *approximate* answer by making a guess and improving it again and again.

The formula is:

```
x_(n+1) = x_n - f(x_n) / f'(x_n)
```

- `x_n` is the current guess
- `x_(n+1)` is the better, next guess
- `f(x_n)` is the value of the function at the guess
- `f'(x_n)` is the derivative (the slope) at the guess

The program repeats this formula until the change between two guesses is smaller than a small number called the **tolerance**.

---

## What the program does

- Takes a function, a starting guess, a tolerance and a maximum number of steps
- Finds the derivative automatically with SymPy
- Repeats the Newton–Raphson formula
- Saves every step in a Pandas table (`iteration_table.csv`)
- Draws 3 graphs with Matplotlib
- Stops safely if the derivative is zero, a value is not a valid number, an input is wrong, or the answer does not converge in time

---

## Example used

| Setting | Value |
|---|---|
| Function | f(x) = x² − 2 |
| Derivative | f'(x) = 2x |
| Starting guess | 2.0 |
| Tolerance | 0.0000000001 (1e-10) |
| Maximum steps | 50 |

The positive root of this equation is √2.

---

## Results (from a real run of the program)

| Step | x_n | x_(n+1) | Error |
|---|---|---|---|
| 1 | 2.000000000000 | 1.500000000000 | 5.0000e-01 |
| 2 | 1.500000000000 | 1.416666666667 | 8.3333e-02 |
| 3 | 1.416666666667 | 1.414215686275 | 2.4510e-03 |
| 4 | 1.414215686275 | 1.414213562375 | 2.1239e-06 |
| 5 | 1.414213562375 | 1.414213562373 | 1.5947e-12 |

- **Approximate root:** 1.414213562373095
- **Iterations used:** 5
- **Final error (size of last step):** 1.595e-12, which is smaller than the tolerance
- **Converged:** Yes

The error gets smaller very quickly. This is called *quadratic convergence*: roughly, the number of correct digits doubles at each step once the guess is close.

Other starting guesses also worked for this function: 1.0 took 5 steps, 1.5 took 4, 10 took 8, 100 took 11, and −3 found the negative root (−√2). A starting guess of 0 stops with a message because the derivative is zero there.

---

## Graphs

| Graph | What it shows |
|---|---|
| `fig1_function.png` | The curve of f(x) with the root marked |
| `fig2_convergence.png` | How the guesses move toward √2 |
| `fig3_error.png` | How the error shrinks (log scale) |
| `fig4_flowchart.png` | Flowchart of the algorithm |

---

## Files in this project

| File | Purpose |
|---|---|
| `newton_raphson.py` | Main program |
| `verify_convergence.py` | Extra check using high-precision numbers |
| `iteration_table.csv` | Table of all iterations from the run |
| `output.txt` | Text printed by the program |
| `verify_output.txt` | Text printed by the check program |
| `fig1_function.png`, `fig2_convergence.png`, `fig3_error.png`, `fig4_flowchart.png` | Graphs and flowchart |

---

## How to run it

1. Install Python 3.
2. Install the libraries:

```
pip install numpy pandas matplotlib sympy
```

3. Run the program:

```
python newton_raphson.py
```

The program prints the table and results, then saves the CSV file and graph images in the same folder.

### Try your own function

Open `newton_raphson.py` and change these lines near the top:

```python
FUNCTION_TEXT = "x**2 - 2"   # write your function using Python style
X0 = 2.0                     # starting guess
TOLERANCE = 1e-10
MAX_ITERATIONS = 50
```

Use `**` for powers, for example `x**3 - 2*x - 5`. The function text is written inside the code by you, so the program does not run unknown text typed by other people.

Note: the titles and labels on the graphs are written for x² − 2, so edit them in `make_graphs` if you change the function.

---

## Libraries used

| Library | Why it is used |
|---|---|
| NumPy | Numbers and values for the graphs |
| Pandas | The iteration table and CSV file |
| Matplotlib | The graphs |
| SymPy | Finds the derivative automatically |

Tested with Python 3.12.3, NumPy 2.4.4, Pandas 3.0.2, Matplotlib 3.10.8 and SymPy 1.14.0.

---

## Limitations

- The results here are for one example function. Other functions may behave differently.
- The method fails if the derivative is zero, and a bad starting guess can be slow or can find a different root.
- The program finds one root per run, and the answer depends on the starting guess.
- Computers store numbers with limited precision, so the last digits can have tiny rounding errors.

---

## References

- Burden, R. L., Faires, J. D., & Burden, A. M. (2016). *Numerical Analysis* (10th ed.). Cengage Learning.
- Harris, C. R., et al. (2020). Array programming with NumPy. *Nature, 585*, 357–362. https://doi.org/10.1038/s41586-020-2649-2
- Hunter, J. D. (2007). Matplotlib: A 2D graphics environment. *Computing in Science & Engineering, 9*(3), 90–95. https://doi.org/10.1109/MCSE.2007.55
- McKinney, W. (2010). Data structures for statistical computing in Python. *Proceedings of the 9th Python in Science Conference*, 56–61. https://doi.org/10.25080/Majora-92bf1922-00a
- Meurer, A., et al. (2017). SymPy: Symbolic computing in Python. *PeerJ Computer Science, 3*, e103. https://doi.org/10.7717/peerj-cs.103


