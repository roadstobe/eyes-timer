# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

`eyes-timer` is a Python 3.14 application managed with `uv`. The project is in early development — `main.py` is the current entry point.

## Commands

```bash
# Install dependencies
uv sync

# Run the app
uv run main.py

# Add a dependency
uv add <package>

# Add a dev dependency
uv add --dev <package>

# Watch for file changes (watchfiles is available as a dev dep)
uv run watchfiles "python main.py" .
```
