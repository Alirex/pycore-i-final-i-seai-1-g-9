# Project Code Conventions

## Main

- Use the latest Python features (e.g., f-strings, type hints).
- Type annotations are required.
- Enforce strict linting and formatting
  rules ([ruff](https://docs.astral.sh/ruff/), [mypy](https://mypy.readthedocs.io/en/stable/)).
  Use [pre-commit](https://pre-commit.com/) for this.
- Use [uv](https://docs.astral.sh/uv/) for dependency management and virtual environments.
- Prefer [pydantic v2](https://docs.pydantic.dev/latest/) for classes, data validation, etc.
- Use `pathlib` for all path manipulations.
- Use [typer](https://typer.tiangolo.com/) for CLI commands.
- Allow use of "grouping" for arguments by "#". Don't use docstring with arguments if annotations are enough.
