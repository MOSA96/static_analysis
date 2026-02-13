# static_analysis

Small Python project that computes the **total cost of sales** from:
- a **price catalog** JSON file
- a **sales record** JSON file

The main script is `compute_sales.py`. It prints results to the console and writes them to `SalesResults.txt`.

---

## Repo structure

```
.
├── compute_sales.py            # CLI script: reads JSON inputs, computes totals, writes SalesResults.txt
├── result_notebook.ipynb       # Example runs + expected results + linter/type-check runs
├── pyproject.toml              # Project metadata + dev tools (flake8, mypy, pylint, ipykernel)
├── uv.lock                     # Locked dependency graph for reproducible installs
├── test_files/                 # Test cases (TC1/TC2/TC3) with sample JSON inputs
├── .python-version             # Python version hint for local tooling
└── .gitignore
```

Notes:
- `pyproject.toml` sets `requires-python = ">=3.12"` and defines dev tools in a dependency group (flake8, mypy, pylint, ipykernel).
- The notebook shows example commands using the test files under `test_files/TC1`, `test_files/TC2`, and `test_files/TC3`.

---

## Prerequisites

- Python **3.12+**
- [uv](https://docs.astral.sh/uv/getting-started/installation/)

---

## Install (recommended: uv sync)

From the repo root:

```bash
uv sync
```

This creates/updates the project virtual environment at `.venv` and installs dependencies from `uv.lock`. By default, `uv sync` performs an “exact” sync (it removes packages not in the lockfile).

---

## Run the script

General usage:

```bash
uv run python compute_sales.py <price_file.json> <sales_file.json>
```

`uv run` executes commands inside the project environment and ensures it is up-to-date before running.

Examples (from the notebook):

```bash
uv run python compute_sales.py test_files/TC1/TC1.ProductList.json test_files/TC1/TC1.Sales.json
uv run python compute_sales.py test_files/TC1/TC1.ProductList.json test_files/TC2/TC2.Sales.json
uv run python compute_sales.py test_files/TC1/TC1.ProductList.json test_files/TC3/TC3.Sales.json
```

Expected totals (from the notebook):

- TC1 → **2481.86**
- TC2 → **166,568.23**
- TC3 → **165,235.37** (includes errors for products missing in the price file)

---

## Dev checks (linting & typing)

Run these from the repo root:

```bash
uv run flake8 compute_sales.py
uv run mypy compute_sales.py
uv run pylint compute_sales.py
```

(These are also demonstrated in `result_notebook.ipynb`.)


## Continuous Integration (Linting & Typing)

This repository includes a GitHub Actions workflow that automatically runs static analysis checks on every `push`.

**Workflow file:**
- `.github/workflows/linters_ci.yml`

**What it does:**
- Checks out the repo
- Installs `uv` and Python (via `uv python install`)
- Installs dependencies using `uv sync`
- Runs:
  - `mypy` (type checking)
  - `pylint` (code quality)
  - `flake8` (linting / style)

The workflow fails if any of these checks fail.
