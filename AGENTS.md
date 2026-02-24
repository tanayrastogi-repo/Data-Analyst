# AGENTS.md - Data Analyst Project

This file contains guidelines and instructions for agentic coding agents working on this repository.

## Project Overview

**Insight-3** is an autonomous LLM agent that ingests structured data (CSV/Excel/Parquet), iteratively writes and executes Python code to explore relationships, and generates insights at three levels (Univariate, Bivariate, Trivariate).

### Tech Stack
- **Package Manager**: `uv`
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

## Project Sprints

### Sprint 1: The "Walking Skeleton" (Foundations & Simple Q/A)

**Theme:** *Plumbing & First Breath*

**Goal:** A functional local application where a user can upload a CSV and ask a free-text question to get a Python-calculated answer.

**Focus:**
- Environment Setup: Initialize `uv` project, set up `marimo` for the UI, and configure Gemini API keys.
- Data Ingestion: Create the logic to read and load a CSV file into a Pandas DataFrame.
- Basic Agent: Build a simple LangGraph node that takes a user query, converts it to Pandas code, and executes it.

**Expected Outcomes:**
- A running `marimo` notebook/app on `localhost`.
- Successful file upload capability (drag-and-drop).
- Feature: "Chat with Data" – The user asks "What is the average age?" and the system returns the correct number by running Python code.
- Tech Deliverable: A `langgraph` workflow with a single "Code Execution" node.

**Sprint 1 User Stories:**
1. **Data Ingestion Interface** - Upload a CSV file via drag-and-drop
2. **Data Preview & Verification** - Display first 5 rows and row/column count
3. **Natural Language Question Answering** - Ask questions in plain English, get calculated answers
4. **Transparency & Verification** - Show the Python code that was executed
5. **Basic Error Handling** - Handle missing columns gracefully without crashing

---

### Sprint 2: The "Automated Inspector" (Level 1 & 2 Analysis)

**Theme:** *Automated Exploration*

**Goal:** The application automatically generates a report covering Column Profiles (Level 1) and Pairwise Relationships (Level 2) upon data upload.

**Focus:**
- Level 1 Logic: Implement loops to iterate through columns. If *Continuous* → calc mean/max/min. If *Discrete* → calc frequency.
- Level 2 Logic: Implement correlation checks. If *Cat + Cont* → GroupBy averages. If *Cat + Cat* → Cross-tabulation.
- Agent Loop: Refine the LangGraph to handle multiple tool calls in sequence.

**Expected Outcomes:**
- Feature: "Auto-Profile" button that generates a structured text summary.
- Feature: Bivariate insights (e.g., "People over 50 have 20% higher Income").
- UI Update: Display insights in expandable sections (Markdown) within the Marimo app.

---

### Sprint 3: The "Deep Diver" (Level 3 Analysis & Self-Correction)

**Theme:** *Complexity & Resilience*

**Goal:** Implement complex 3-variable analysis and ensure the agent is robust enough to fix its own coding errors.

**Focus:**
- Level 3 Logic: Implement prompt logic to look for interactions (e.g., using Decision Trees to find rules like `IF Age > X AND License = Yes THEN...`).
- Error Handling (Self-Correction): Update LangGraph. If the code execution tool returns a `Python Error`, loop back to the LLM with the error message to regenerate the code.
- Visuals: Allow the agent to generate simple charts (matplotlib/seaborn) to support its insights.

**Expected Outcomes:**
- Feature: Complete "Level 3 Insight" generation (A + B → C relationships).
- Feature: Self-healing agents (The logs show the agent fixing a `KeyError` or `SyntaxError` automatically).
- Feature: Charts embedded in the insights (e.g., a scatter plot showing the 3-variable relationship).

---

### Sprint 4: The "Cloud Commander" (Deployment & Polish)

**Theme:** *Production & Shipping*

**Goal:** A secure, publicly accessible URL where users can access the application, hosted on the Cloud.

**Focus:**
- Containerization: Create a `Dockerfile` that packages `uv`, `marimo`, and the Python runtime.
- Infrastructure: Deploy to a cloud provider (e.g., **Google Cloud Run**).
- Security: Ensure API keys are injected via Environment Variables (Secrets Management).
- Testing: Finalize `pytest` suite to ensure the "Analyst" doesn't hallucinate on standard test datasets.

**Expected Outcomes:**
- Deliverable: A live public URL (e.g., `https://my-data-analyst.run.app`).
- Deliverable: CI/CD pipeline (GitHub Actions) that runs tests when code is pushed.
- User Experience: A polished UI with loading states (spinners) while the agent is "thinking/coding."

---

## The 3 Levels of Analysis

### Level 1: Univariate Analysis (Column Profiling)
- **Goal:** Characterize every single column independently.
- **Logic:**
  - *Continuous:* Calculate Min, Max, Mean, Median, Std Dev, Distribution shape.
  - *Discrete/Categorical:* Get Unique counts, Top 5 most frequent values with percentages.
  - *Missing Data:* Count and percentage of nulls.

### Level 2: Bivariate Analysis (Pairwise Relationships)
- **Goal:** Identify strong correlations or conditional rules between *pairs* of columns ($A \rightarrow B$).
- **Logic:** Generate Python code to calculate correlation matrices (Pearson/Spearman) or run Chi-Square tests.
- **Output Format:** "If `Column A` is [Condition], then `Column B` tends to be [Result]."

### Level 3: Trivariate Analysis (Multi-Factor Interactions)
- **Goal:** Detect complex patterns involving *three* variables ($A + B \rightarrow C$).
- **Logic:** Look for confounding variables or interaction effects (e.g., using Decision Trees).
- **Output Format:** "If `Column A` is [Condition 1] AND `Column B` is [Condition 2], then `Column C` is [Result]."

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
```
src/
├── __init__.py
├── agent/
│   ├── __init__.py
│   ├── state.py          # LangGraph state definitions
│   ├── nodes.py          # Graph nodes (LoadData, Analyze, etc.)
│   └── graph.py          # Graph construction
├── utils/
│   ├── __init__.py
│   ├── data_loader.py    # CSV/Parquet loading
│   └── code_executor.py  # Safe code execution
└── config.py             # Configuration settings

tests/
├── __init__.py
├── test_agent/           # Agent tests
├── test_utils/           # Utility tests
└── conftest.py           # Pytest fixtures

agent_app.py              # Main Marimo notebook entry
pyproject.toml            # Project configuration
```

### LangGraph Guidelines
- Define clear state schemas using `TypedDict`.
- Create modular nodes with single responsibilities.
- Use proper state transitions and conditional edges.
- Handle recursion limits with error nodes.

```python
from typing import TypedDict

class AgentState(TypedDict):
    df: pd.DataFrame
    insights: list[str]
    error: str | None
```

### Testing Guidelines
- Place tests in `tests/` directory mirroring `src/` structure.
- Use descriptive test names: `test_load_csv_returns_dataframe_for_valid_file`.
- Use fixtures for common setup (e.g., sample DataFrames).
- Test edge cases and error conditions, not just happy paths.

```python
import pytest
import pandas as pd
from src.utils.data_loader import load_csv

def test_load_csv_returns_dataframe_for_valid_file(tmp_path):
    csv_file = tmp_path / "test.csv"
    csv_file.write_text("a,b\n1,2\n3,4")
    
    result = load_csv(str(csv_file))
    
    assert isinstance(result, pd.DataFrame)
    assert result.shape == (2, 2)
```

### Marimo Notebook Guidelines
- Keep notebooks reactive and stateless where possible.
- Use `mo.ui` for interactive elements.
- Separate logic into `src/` modules, import into notebooks.

---

## Key System Instructions

When working as the LLM agent:

> **Role**: "You are an Expert Python Data Analyst. You do not guess; you verify. You answer questions by writing executable Python code using `pandas`, executing it, and interpreting the printed output."

> **Level 3 Analysis Constraint**: "When looking for Level 3 insights (3 variables), avoid stating the obvious. Focus on 'Interaction Effects' where the relationship between A and C changes depending on B. Use decision tree logic (e.g., `sklearn.tree.DecisionTreeClassifier` with max_depth=3) to find these splits automatically."

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
