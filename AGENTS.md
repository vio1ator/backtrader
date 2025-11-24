# Repository Guidelines

## Project Structure & Modules
- Core library lives in `backtrader/` (engine, feeds, brokers, indicators, analyzers, observers, plotting).
- CLI entry points: `backtrader/btrun/btrun.py` exposed as `btrun`/`bt-run`; legacy helper `tools/bt-run.py`.
- Tests in `tests/` (indicator coverage, broker/order/strategy basics). Sample scripts in `samples/`, contrib tools in `contrib/`, datasets in `datas/`.
- Packaging: `pyproject.toml` with setuptools backend; `uv` is preferred for installs/builds.

## Build, Test, and Development Commands
- Install editable for development: `uv pip install -e .`
- Run full test suite: `uv run pytest`
- Build distributions: `uv build` (outputs to `dist/`)
- Publish (manual): `uv run --with twine twine upload dist/*`
- CI uses GitHub Actions (`.github/workflows/ci.yml`) with Python 3.9–3.12 via `uv`.

## Coding Style & Naming
- Python 3.9+ only; drop Python 2 shims.
- Indentation: 4 spaces; keep ASCII in sources unless necessary.
- Naming: classes `CamelCase`, functions/vars `snake_case`; prefer f-strings over `%` formatting.
- Imports: avoid wildcard imports in new code; keep module-relative imports consistent with existing layout.
- Add concise comments only where behavior is non-obvious.

## Testing Guidelines
- Framework: `pytest`; existing suites emphasize indicators and core behaviors.
- Test files reside in `tests/` and follow `test_*.py`; add focused unit tests near related modules.
- Run `uv run pytest` before submitting; consider adding filterwarnings to reduce noise when adding new tests.

## Commit & Pull Request Guidelines
- Commit messages in git history are short, imperative summaries (e.g., “Fix errors for simulated orders”); follow that style.
- For PRs: describe the change, list key areas touched (`backtrader/...`, `tests/...`), include test command/output, and note any new extras/deps.
- Link related issues and include screenshots only when UI/plot output changes.

## Security & Configuration Tips
- No secrets in repo; do not commit credentials for brokers/data sources.
- Optional dependencies (matplotlib, pandas, TA-Lib, IB/Oanda clients) should be declared via extras in `pyproject.toml` and documented in PRs.
