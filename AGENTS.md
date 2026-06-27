# AGENTS.md

## Role of Agents

This repository follows automated AI-assisted development standards.

## Rules

* Always run tests before committing
* Use ruff for linting and formatting
* Use mypy for type checking
* Ensure pip-audit passes before release

## CI Requirements

* All GitLab CI jobs must pass:

  * lint
  * format
  * test
  * type\_check
  * coverage

## Quality Standards

* No code without tests
* No untyped public functions
* No secrets in repository

