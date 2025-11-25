# UV Local Development Setup Guide

A comprehensive guide for using **uv** - the ultra-fast Python package and project manager by Astral.

## Table of Contents

1. [What is uv?](#what-is-uv)
2. [Installation](#installation)
3. [Basic Workflow](#basic-workflow)
4. [Working with Projects](#working-with-projects)
5. [Running Scripts](#running-scripts)
6. [Managing Dependencies](#managing-dependencies)
7. [Python Version Management](#python-version-management)
8. [Best Practices](#best-practices)
9. [Common Commands Cheat Sheet](#common-commands-cheat-sheet)

---

## What is uv?

**uv** is an extremely fast Python package and project manager written in Rust. It replaces multiple tools:
- `pip` - Package installation
- `pip-tools` - Dependency management
- `virtualenv` - Virtual environment creation
- `pyenv` - Python version management
- `poetry`/`pipenv` - Project management

**Key Benefits:**
- ⚡ **10-100x faster** than pip
- 🔒 **Built-in lockfiles** for reproducible installs
- 🐍 **Python version management** included
- 📦 **Project-aware** dependency resolution
- 🚀 **Single binary** - no dependencies required

---

## Installation

### macOS and Linux

Using the standalone installer (recommended):

```bash
# Download and install
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Using Homebrew:

```bash
brew install uv
```

### Windows

Using PowerShell:

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Using WinGet:

```powershell
winget install --id=astral-sh.uv -e
```

### Alternative Methods

**PyPI (via pipx - recommended):**
```bash
pipx install uv
```

**PyPI (via pip):**
```bash
pip install uv
```

### Verify Installation

```bash
uv --version
# Output: uv 0.9.11 (or latest version)
```

### Enable Shell Autocompletion (Optional)

**Bash:**
```bash
echo 'eval "$(uv generate-shell-completion bash)"' >> ~/.bashrc
source ~/.bashrc
```

**Zsh:**
```bash
echo 'eval "$(uv generate-shell-completion zsh)"' >> ~/.zshrc
source ~/.zshrc
```

**Fish:**
```bash
echo 'uv generate-shell-completion fish | source' > ~/.config/fish/completions/uv.fish
```

---

## Basic Workflow

### Quick Start

```bash
# 1. Create a new project
uv init my-project
cd my-project

# 2. Add dependencies
uv add requests pandas

# 3. Run your code
uv run main.py

# 4. Sync dependencies (optional - happens automatically)
uv sync
```

That's it! uv handles virtual environments, lockfiles, and dependency installation automatically.

---

## Working with Projects

### Create a New Project

**Standard project:**
```bash
uv init my-project
cd my-project
```

**In current directory:**
```bash
mkdir my-project
cd my-project
uv init
```

**Application with package structure:**
```bash
uv init --app --package my-cli-app
```

### Project Structure

After running `uv init` and `uv run`, your project will look like:

```
my-project/
├── .venv/              # Virtual environment (auto-created)
├── .python-version     # Python version pin
├── .gitignore         # Git ignore rules
├── README.md          # Project documentation
├── main.py            # Entry point
├── pyproject.toml     # Project metadata & dependencies
└── uv.lock            # Lockfile (auto-generated)
```

### Understanding Key Files

**pyproject.toml** - Project configuration:
```toml
[project]
name = "my-project"
version = "0.1.0"
description = "My awesome project"
dependencies = [
    "requests>=2.31.0",
    "pandas>=2.0.0",
]

[tool.uv]
# uv-specific configuration
dev-dependencies = [
    "pytest>=7.4.0",
]
```

**uv.lock** - Dependency lockfile:
- Contains exact versions of all dependencies
- Ensures reproducible installations
- Auto-generated and managed by uv
- **Should be committed to version control**

**.python-version** - Python version:
```
3.11.0
```

---

## Running Scripts

### Simple Scripts (No Dependencies)

```python
# hello.py
print("Hello, world!")
```

```bash
uv run hello.py
# Output: Hello, world!
```

### Scripts with Dependencies

**Method 1: Using --with flag**

```python
# example.py
import requests
response = requests.get("https://api.github.com")
print(response.status_code)
```

```bash
uv run --with requests example.py
```

**Method 2: Inline script metadata (Recommended)**

Create script with inline dependencies:

```bash
uv init --script example.py --python 3.12
```

Add dependencies to the script:

```bash
uv add --script example.py requests rich
```

This creates:

```python
# /// script
# requires-python = ">=3.12"
# dependencies = [
#   "requests",
#   "rich",
# ]
# ///

import requests
from rich import print

response = requests.get("https://api.github.com")
print(response.json())
```

Run it:

```bash
uv run example.py
```

### Executable Scripts with Shebang

```python
#!/usr/bin/env -S uv run --script
# /// script
# dependencies = ["httpx"]
# ///

import httpx
print(httpx.get("https://example.com"))
```

Make it executable:

```bash
chmod +x script.py
./script.py
```

---

## Managing Dependencies

### Adding Dependencies

**Add a package:**
```bash
uv add requests
```

**Add with version constraint:**
```bash
uv add "requests>=2.31.0,<3.0.0"
uv add "pandas==2.0.3"
```

**Add from Git:**
```bash
uv add git+https://github.com/psf/requests
```

**Add from requirements.txt:**
```bash
uv add -r requirements.txt
```

**Add development dependencies:**
```bash
uv add --dev pytest black mypy
```

### Removing Dependencies

```bash
uv remove requests
```

### Upgrading Dependencies

**Upgrade a specific package:**
```bash
uv lock --upgrade-package requests
```

**Upgrade all packages:**
```bash
uv lock --upgrade
```

### Installing Dependencies

**Install project dependencies:**
```bash
uv sync
```

**Install with dev dependencies:**
```bash
uv sync --all-extras
```

**Install without dev dependencies:**
```bash
uv sync --no-dev
```

### Exporting Dependencies

**Export to requirements.txt:**
```bash
uv export --format requirements-txt > requirements.txt
```

**Export with hashes:**
```bash
uv export --format requirements-txt --no-hashes > requirements.txt
```

---

## Python Version Management

### Install Python Versions

```bash
# Install specific version
uv python install 3.12

# Install multiple versions
uv python install 3.11 3.12 3.13

# Install latest patch version
uv python install 3.12
```

### List Python Versions

```bash
# List installed versions
uv python list

# List available versions
uv python list --all-versions
```

### Use Specific Python Version

**For current project:**
```bash
# Set in .python-version
echo "3.12" > .python-version

# Or specify in pyproject.toml
# [project]
# requires-python = ">=3.12"
```

**For a single command:**
```bash
uv run --python 3.11 main.py
```

**Check current Python:**
```bash
uv run python --version
```

---

## Best Practices

### 1. **Always Use Projects for Multi-File Code**

```bash
# ✅ Good: Create a project
uv init my-app
cd my-app
uv add requests
uv run main.py

# ❌ Avoid: Manual virtual environment management
python -m venv venv
source venv/bin/activate
pip install requests
```

### 2. **Commit uv.lock to Version Control**

```bash
git add uv.lock pyproject.toml
git commit -m "Lock dependencies"
```

This ensures everyone on your team uses identical dependency versions.

### 3. **Use Inline Metadata for Standalone Scripts**

```python
# ✅ Good: Self-contained script
# /// script
# dependencies = ["requests"]
# ///
import requests
```

```bash
# ❌ Avoid: Implicit dependencies
# Requires manual: pip install requests
import requests
```

### 4. **Pin Python Version in .python-version**

```bash
echo "3.12.0" > .python-version
```

This ensures consistent Python versions across environments.

### 5. **Use uv run Instead of Activating Environments**

```bash
# ✅ Good: No activation needed
uv run pytest
uv run python -m flask run

# ❌ Old way: Manual activation
source .venv/bin/activate
pytest
python -m flask run
```

### 6. **Separate Dev Dependencies**

```bash
# Production dependencies
uv add requests pandas

# Development dependencies
uv add --dev pytest black mypy ruff
```

In `pyproject.toml`:
```toml
[project]
dependencies = ["requests", "pandas"]

[tool.uv]
dev-dependencies = ["pytest", "black", "mypy"]
```

### 7. **Use Configuration in pyproject.toml**

```toml
[tool.uv]
# Use specific index
index-url = "https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple"

# Exclude newer packages (reproducibility)
exclude-newer = "2024-01-01T00:00:00Z"
```

### 8. **Update uv Regularly**

```bash
# Self-update (if installed via standalone installer)
uv self update

# Or via package manager
brew upgrade uv
pipx upgrade uv
```

---

## Common Commands Cheat Sheet

### Project Management

| Command | Description |
|---------|-------------|
| `uv init` | Create new project in current directory |
| `uv init my-project` | Create new project in new directory |
| `uv sync` | Install dependencies from lockfile |
| `uv lock` | Update lockfile without installing |
| `uv run <command>` | Run command in project environment |
| `uv build` | Build distribution packages |

### Dependency Management

| Command | Description |
|---------|-------------|
| `uv add <package>` | Add dependency |
| `uv add --dev <package>` | Add dev dependency |
| `uv remove <package>` | Remove dependency |
| `uv lock --upgrade` | Upgrade all dependencies |
| `uv lock --upgrade-package <pkg>` | Upgrade specific package |
| `uv export` | Export dependencies to requirements.txt |

### Python Management

| Command | Description |
|---------|-------------|
| `uv python install 3.12` | Install Python 3.12 |
| `uv python list` | List installed Python versions |
| `uv python pin 3.12` | Pin Python version for project |
| `uv run --python 3.11 <cmd>` | Run with specific Python version |

### Script Management

| Command | Description |
|---------|-------------|
| `uv init --script file.py` | Create script with inline metadata |
| `uv add --script file.py <pkg>` | Add dependency to script |
| `uv run --with <pkg> file.py` | Run script with temporary dependency |
| `uv run file.py` | Run script with inline dependencies |

### Other Commands

| Command | Description |
|---------|-------------|
| `uv --version` | Show uv version |
| `uv self update` | Update uv itself |
| `uv cache clean` | Clear package cache |
| `uv pip install <pkg>` | Use uv as pip replacement |

---

## Migrating from Other Tools

### From pip + venv

**Before:**
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

**After:**
```bash
uv init
uv add -r requirements.txt
uv run main.py
```

### From Poetry

**Before:**
```bash
poetry install
poetry add requests
poetry run python main.py
```

**After:**
```bash
uv sync
uv add requests
uv run python main.py
```

### From Pipenv

**Before:**
```bash
pipenv install
pipenv install requests
pipenv run python main.py
```

**After:**
```bash
uv sync
uv add requests
uv run python main.py
```

---

## Troubleshooting

### Issue: "Python version not found"

**Solution:**
```bash
# Install required Python version
uv python install 3.12
```

### Issue: "Lockfile out of sync"

**Solution:**
```bash
# Update lockfile
uv lock
```

### Issue: "Cache issues"

**Solution:**
```bash
# Clear cache
uv cache clean
```

### Issue: "Want to use system Python"

**Solution:**
```bash
# Use --system flag
uv run --system python main.py
```

---

## Additional Resources

- **Official Documentation**: https://docs.astral.sh/uv/
- **GitHub Repository**: https://github.com/astral-sh/uv
- **Getting Started Guide**: https://docs.astral.sh/uv/getting-started/
- **Project Guide**: https://docs.astral.sh/uv/guides/projects/
- **Scripts Guide**: https://docs.astral.sh/uv/guides/scripts/

---

## Summary

**Key Takeaways:**

1. ✅ **Use `uv init`** to create projects
2. ✅ **Use `uv add`** to manage dependencies
3. ✅ **Use `uv run`** to execute code (no activation needed)
4. ✅ **Commit `uv.lock`** to version control
5. ✅ **Pin Python version** in `.python-version`
6. ✅ **Use inline metadata** for standalone scripts

**Why uv?**
- 🚀 Blazing fast (10-100x faster than pip)
- 🔒 Reproducible builds with lockfiles
- 🐍 Built-in Python version management
- 📦 Replaces multiple tools (pip, venv, pyenv, poetry)
- 🎯 Zero configuration for simple projects

Start using uv today and never look back! 🎉
