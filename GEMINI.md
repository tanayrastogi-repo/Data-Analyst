# AGENTS.md - Data Analyst Project

This file contains guidelines and instructions for agentic coding agents working on this repository.

## Project Overview

**Insight-3** is an autonomous LLM agent that ingests structured data (CSV/Excel/Parquet), iteratively writes and executes Python code to explore relationships, and generates insights at three levels (Univariate, Bivariate, Trivariate).

### Tech Stack
- **Package Manager**: `uv`
- **Data Processing**: `polars` (instead of pandas)
- **Development Notebook**: `marimo`
- **Orchestration**: `LangGraph`
- **LLM Provider**: Google Gemini (via `GEMINI_API_KEY`)
- **Testing**: `pytest`
- **ML**: `scikit-learn` (for Level 3 decision tree analysis)

---

## Commands

### Environment Setup
```bash
# Install dependencies using uv
uv sync

# Activate virtual environment
source .venv/bin/activate  # or `uv shell` on Windows
```

### Running the Application
```bash
# Run Marimo notebook
marimo edit
# or
marimo run agent_app.py
```

### Testing
```bash
# Run all tests
pytest

# Run tests with verbose output
pytest -v

# Run a single test file
pytest tests/test_file.py

# Run a single test function
pytest tests/test_file.py::test_function_name

# Run tests matching a pattern
pytest -k "test_pattern"

# Run tests with coverage
pytest --cov=src --cov-report=html
```

### Linting & Type Checking
```bash
# Run ruff linter
ruff check .

# Auto-fix linting issues
ruff check --fix .

# Run mypy type checker
mypy .

# Run all checks (ruff + mypy)
ruff check . && mypy .
```

### Code Formatting
```bash
# Format code with ruff
ruff format .
```


---

## Code Style Guidelines

### General Principles
- Write **executable, verified code** - never guess; always verify with actual data calculations.
- Use **type hints** throughout for clarity and static analysis.
- Keep functions small and focused (single responsibility).
- Add docstrings to all public functions and classes.

### Imports
- Use absolute imports (e.g., `from src.utils import helper`).
- Group imports in this order: standard library, third-party, local application.
- Sort imports alphabetically within each group.
- Use `ruff` for automatic import sorting.

```python
# Correct import order
import os
import sys
from collections.abc import Iterator
from pathlib import Path

import pandas as pd
from langgraph.graph import StateGraph

from src.agent.nodes import LoadData, GenerateSummary
```

### Naming Conventions
- **Variables/functions**: `snake_case` (e.g., `load_data`, `dataframe`)
- **Classes**: `PascalCase` (e.g., `DataProfiler`, `InsightSynthesizer`)
- **Constants**: `UPPER_SNAKE_CASE` (e.g., `MAX_ROWS`, `DEFAULT_TIMEOUT`)
- **Private variables**: prefix with underscore (e.g., `_internal_state`)
- Use descriptive names that convey intent (e.g., `correlation_matrix` not `mat`)

### Type Hints
- Always use type hints for function parameters and return values.
- Use `Optional[X]` instead of `X | None` for Python 3.9 compatibility, or use union syntax for 3.10+.
- Be specific with types (e.g., `list[int]` not `list`).

```python
# Good
def analyze_column(df: pd.DataFrame, column: str) -> dict[str, float]:
    """Analyze a single column and return statistics."""
    pass

# Avoid
def analyze_column(df, column):
    """Analyze a column."""
    pass
```

### Error Handling
- Use specific exception types (e.g., `ValueError`, `FileNotFoundError`).
- Always include helpful error messages.
- Handle errors gracefully in the agent loop - catch, log, and allow retry.

```python
# Good
def load_csv(path: str) -> pd.DataFrame:
    if not Path(path).exists():
        raise FileNotFoundError(f"Data file not found: {path}")
    try:
        return pd.read_csv(path)
    except pd.errors.EmptyDataError:
        raise ValueError(f"CSV file is empty: {path}")
```

### File Organization

**IMPORTANT:** All application code, utility functions, and tests must be written within `agent_app.py` using Marimo cells. Do NOT create separate folders or scripts for utils or tests.

```
project/
├── agent_app.py              # All code (UI, utils, tests in cells)
├── pyproject.toml            # Project configuration
├── .env                      # Environment variables
├── data/                     # Data files
│   └── temp/                 # Temporary uploaded files
```

### Marimo Notebook Guidelines
- Keep notebooks reactive and stateless where possible.
- Use `mo.ui` for interactive elements.
- Write all utility functions in dedicated "Utils" cells (marked with `@app.cell(hide_code=True)` for section headers).
- Write all tests in dedicated "Tests" cells.
- Use the cell structure shown in `agent_app.py`:
  - Import cell for marimo
  - Title cell (hide_code)
  - UI components (file upload, buttons, etc.)
  - Logic cells that depend on UI components
  - Utils cell for helper functions
  - Tests cell for test classes

```python
# Example structure in agent_app.py
@app.cell
def _(mo):
    # UI components
    upload = mo.ui.file(...)
    upload
    return (upload,)

@app.cell
def _(mo, upload):
    # Logic using upload
    if upload.value:
        ...

@app.cell(hide_code=True)
def _(mo):
    mo.md("## Utils")  # Section header
    return

@app.cell
def _():
    # Utility functions
    def my_helper():
        ...
    return my_helper

@app.cell(hide_code=True)
def _(mo):
    mo.md("## Tests")
    return

@app.cell
def _():
    # Test classes
    class TestMyCode:
        ...
    return
```

---

## Testing Guidelines

- Write tests within `agent_app.py` in dedicated test cells (not in separate files).
- Use descriptive test names following pytest conventions.
- Test edge cases and error conditions, not just happy paths.
- Run tests using Marimo's built-in test execution or pytest.

---

## Development Workflow

1. **Create branch**: `git checkout -b feature/your-feature`
2. **Write code** following style guidelines
3. **Run tests**: `pytest -v`
4. **Run linters**: `ruff check . && mypy .`
5. **Format code**: `ruff format .`
6. **Commit changes** (if requested)

---

## Configuration

- Store API keys in environment variables (`GEMINI_API_KEY`).
- Use `pyproject.toml` for project metadata and dependencies.
- Configure `ruff` and `mypy` in `pyproject.toml` or separate config files.
