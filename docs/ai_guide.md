# AI Guide

## Workflow

1. **Plan**: describe the change in small steps.
2. **Diff**: implement minimal edits without refactors.
3. **Tests**: run the relevant tests and report results.

## PR Discipline

- Keep PRs small and focused.
- Use clear commit messages.
- Update docs when behavior changes.

## Bugs

- Add tests first when fixing bugs.
- Validate determinism if RNG or chunk generation changes.

## Linting & Formatting

- Use `ruff` for linting and formatting.
- Maintain typing for core/simulation/content modules.
- Keep docstrings concise and accurate.

## Definition of Done

- Tests pass.
- Lint passes.
- Docs updated for any public API change.
