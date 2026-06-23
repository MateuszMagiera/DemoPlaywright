# Ruff + Pre-Commit Setup Guide

## ✅ Installation Complete

Your project now has **ruff** and **pre-commit** configured and ready to use.

### 📦 Installed Packages

- **ruff** (v0.15.18) — Fast Python linter & formatter
- **pre-commit** (v4.6.0) — Git hook framework
- **pytest** (v9.1.1) — Testing framework

All installed in `.venv/` virtual environment.

---

## 📂 New Files Created

### 1. `pyproject.toml` — Python project config
- Ruff configuration (100 char line length, Python 3.9+)
- Linting rules (pycodestyle, pyflakes, isort, flake8-bugbear)
- Project metadata

### 2. `.pre-commit-config.yaml` — Pre-commit hook definitions
- **ruff** — Auto-fix code formatting issues
- **ruff-format** — Format code style (PEP 8)
- **trailing-whitespace** — Remove trailing spaces
- **end-of-file-fixer** — Fix missing newlines
- **check-yaml** — Validate YAML files
- **check-added-large-files** — Prevent large file commits
- **detect-private-key** — Catch accidental secrets

### 3. `requirements-dev.txt` — Development dependencies
- ruff, pre-commit, pytest
- Easy `pip install -r requirements-dev.txt` for other developers

### 4. `.gitignore` — Git ignore patterns
- Python cache files (`__pycache__/`, `*.pyc`)
- Virtual environments
- IDE configs
- Test coverage
- OS files

### 5. `.git/` directory (Git repository)
- Initialized empty repo
- Pre-commit hooks installed at `.git/hooks/pre-commit`

---

## 🎯 How It Works

### Git Workflow

```
1. You make changes to files
   ↓
2. Run: git commit -m "message"
   ↓
3. Pre-commit hooks trigger automatically:
   ├─ ruff auto-fixes code style
   ├─ ruff-format formats code
   ├─ Removes trailing whitespace
   ├─ Fixes end-of-file issues
   ├─ Validates YAML syntax
   └─ Checks for secrets
   ↓
4. If hooks modified files → modify staging area
   ↓
5. Commit succeeds if all checks pass
   ↓
6. Commit rejected if security issues found
```

### First Run Example

On first commit, pre-commit hooks initialize themselves (downloads ruff, pre-commit hooks environments):

```
[INFO] Initializing environment for https://github.com/astral-sh/ruff-pre-commit.
[INFO] Initializing environment for https://github.com/pre-commit/pre-commit-hooks.
[INFO] Installing environment for https://github.com/astral-sh/ruff-pre-commit.
```

**This happens once. Subsequent commits are fast.**

---

## 📝 Available Commands

### Run Ruff Manually

```bash
# Check for issues (no fix)
ruff check .

# Fix issues automatically
ruff check . --fix

# Format code
ruff format .

# Combined: check + format
ruff check . --fix && ruff format .
```

### Run Pre-Commit

```bash
# Run all hooks on staged files (automatic on commit)
git commit -m "..."

# Run all hooks on all files
pre-commit run --all-files

# Run specific hook
pre-commit run ruff --all-files

# Update hook definitions
pre-commit autoupdate
```

### Run Tests

```bash
# Run pytest
pytest

# Verbose output
pytest -v

# With coverage
pytest --cov
```

---

## 🔧 Configuration Details

### Ruff Lint Rules in `pyproject.toml`

**Selected rules:**
- `E` — pycodestyle errors (indentation, whitespace, etc.)
- `W` — pycodestyle warnings
- `F` — pyflakes (undefined names, unused imports, etc.)
- `I` — isort (import sorting)
- `C` — flake8-comprehensions (list/dict/set comprehensions)
- `B` — flake8-bugbear (likely bugs)

**Ignored rules:**
- `E501` — Line too long (handled by line-length setting)
- `W191` — Indentation contains tabs

**Line length:** 100 characters

---

## 👥 For Team Members

**Onboarding checklist:**

1. Clone repo
2. Create virtual environment: `python -m venv .venv`
3. Activate: `.venv\Scripts\activate` (Windows) or `source .venv/bin/activate` (Mac/Linux)
4. Install dev dependencies: `pip install -r requirements-dev.txt`
5. Pre-commit hooks auto-installed on first commit

**No extra setup needed.** Hooks run automatically on commit.

---

## ⚙️ Customization

### Change Ruff Line Length

Edit `pyproject.toml`:

```toml
[tool.ruff]
line-length = 88  # Change from 100
```

### Add More Lint Rules

Edit `pyproject.toml`:

```toml
[tool.ruff.lint]
select = [
    "E", "W", "F", "I", "C", "B",
    "D",  # docstrings (pydocstyle)
    "UP", # pyupgrade
]
```

### Disable Pre-Commit Temporarily

```bash
# Bypass hooks on commit (not recommended!)
git commit --no-verify -m "..."
```

### Update Hook Versions

```bash
pre-commit autoupdate
git add .pre-commit-config.yaml
git commit -m "chore: update pre-commit hooks"
```

---

## 🚨 Common Issues

**Q: "pre-commit hook failed"**
A: Ruff found issues. Run `ruff check . --fix` to auto-fix. Re-stage and commit.

**Q: "Black/isort conflict"**
A: Ruff handles both. No conflicts. Just use ruff.

**Q: "Hook executable not found"**
A: Delete `.venv/` and reinstall: `pip install -r requirements-dev.txt`

**Q: "My IDE doesn't respect ruff config"**
A: Open IDE settings, point to `pyproject.toml`. VS Code: Install Ruff extension, set `ruff.pythonPath`.

---

## 📊 Status Check

Current state:

```
✅ Git repo initialized (.git/)
✅ Ruff installed (v0.15.18)
✅ Pre-commit installed (v4.6.0)
✅ Pytest installed (v9.1.1)
✅ Pre-commit hooks active (.git/hooks/pre-commit)
✅ Config files created (pyproject.toml, .pre-commit-config.yaml)
✅ Initial commit made (b69f9d5)
✅ All hooks passed on commit
```

---

## 🔗 Links

- **Ruff docs:** https://docs.astral.sh/ruff/
- **Pre-commit docs:** https://pre-commit.com/
- **Pytest docs:** https://docs.pytest.org/

---

## ✨ Next Steps

1. **Add more specific rules** — Uncomment docstring checks, upgrade checks, etc. in `pyproject.toml`
2. **Create Python modules** — Start writing code; hooks will auto-check on commit
3. **Add GitHub Actions** — Auto-run hooks on PRs (optional)
4. **Share with team** — Push to GitHub; team clones + `pip install -r requirements-dev.txt`

---

**Everything is ready. Start coding! ⛏**

Hooks run automatically on every commit. No friction. Clean code by default.
