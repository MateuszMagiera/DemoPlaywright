# DemoPlaywright — QA Automation Showcase

> **Python + Playwright** portfolio project demonstrating senior-level test automation across
> functional, security, performance, accessibility, AI testing and more.

[![CI](https://github.com/user/DemoPlaywright/actions/workflows/tests.yml/badge.svg)](https://github.com/user/DemoPlaywright/actions)
[![Phase](https://img.shields.io/badge/Phase-1%20Complete-brightgreen)](#phases)

---

## 🚀 Quick Start

```bash
# 1. Clone & create venv
git clone https://github.com/user/DemoPlaywright.git
cd DemoPlaywright
python -m venv .venv
.venv\Scripts\activate          # Windows
# source .venv/bin/activate     # Linux/Mac

# 2. Install dependencies
pip install -r requirements-dev.txt
playwright install

# 3. Copy env config
cp .env.example .env

# 4. Run smoke tests
pytest tests/functional/ -m smoke -v

# 5. Run all tests (excluding slow)
pytest tests/functional/ -m "not slow"

# 6. Generate HTML report
pytest tests/functional/ -m "not slow" --html=reports/report.html --self-contained-html
```

---

## 📁 Project Structure

```
src/
├── config.py                     # pydantic-settings config (BROWSER, HEADLESS, etc.)
└── pages/
    ├── base_page.py              # BasePage — typed helpers for all page objects
    ├── forms/
    │   ├── text_box_page.py      # TextBox form POM
    │   ├── checkbox_page.py      # CheckBox tree POM (rc-tree widget)
    │   └── radio_button_page.py  # RadioButton POM
    ├── widgets/
    │   ├── slider_page.py        # Slider widget POM
    │   ├── progress_bar_page.py  # Progress bar POM
    │   └── tabs_page.py          # Tabs widget POM
    └── alerts/
        ├── alerts_page.py        # Alert dialogs POM
        └── browser_windows_page.py  # Multi-tab/window POM
tests/
└── functional/
    ├── conftest.py               # Page object fixtures
    ├── test_forms.py             # TextBox, CheckBox, RadioButton tests
    ├── test_widgets.py           # Slider, ProgressBar, Tabs tests
    └── test_alerts.py            # Alert, Confirm, Prompt, Window tests
conftest.py                       # Root: browser, context, page fixtures + screenshot on fail
pyproject.toml                    # pytest config, ruff, mypy settings
```

---

## ✅ Running Tests

```bash
# Smoke tests only (fast, happy-path)
pytest tests/functional/ -m smoke -v

# Full functional suite (excluding slow)
pytest tests/functional/ -m "not slow" -v

# Specific test class
pytest tests/functional/test_forms.py::TestTextBox -v

# With Allure report
pytest tests/functional/ -m "not slow" --alluredir=reports/allure-results
allure serve reports/allure-results

# With HTML report
pytest tests/functional/ -m "not slow" --html=reports/report.html --self-contained-html

# All tests including slow (progress bar waits)
pytest tests/functional/ -v
```

---

## ⚙️ Configuration

Copy `.env.example` to `.env` and edit:

| Variable | Default | Description |
|----------|---------|-------------|
| `BROWSER` | `chromium` | Browser: chromium / firefox / webkit |
| `HEADLESS` | `true` | Run headless (false = visible browser) |
| `SLOW_MO` | `0` | Slow motion delay between actions (ms) |
| `DEFAULT_TIMEOUT` | `30000` | Default element timeout (ms) |
| `TRACING` | `retain-on-failure` | Playwright tracing: off / on / retain-on-failure |
| `VIDEO` | `retain-on-failure` | Video recording mode |

---

## 🧪 Test Markers

| Marker | Description |
|--------|-------------|
| `@pytest.mark.smoke` | Fast happy-path — run on every push |
| `@pytest.mark.regression` | Full regression suite |
| `@pytest.mark.slow` | Tests > 10s (progress bar, timers) |
| `@pytest.mark.functional` | UI / E2E tests |
| `@pytest.mark.api` | API-layer tests (no browser) |
| `@pytest.mark.security` | Security & penetration tests |
| `@pytest.mark.performance` | Load / stress tests |

---

## 📊 Phase Progress

| Phase | Status | Area | Key Skills |
|-------|--------|------|-----------|
| **1 — Foundation** | ✅ Done | Functional E2E | POM, fixtures, type hints, parallel |
| 2 — API Testing | 🔜 Next | API + Contract | httpx, pydantic, Pact |
| 3 — Reporting | ⏳ Planned | Observability | Allure, structlog, Slack |
| 4 — CI/CD | ⏳ Planned | DevOps | GitHub Actions, Pages |
| 5 — Performance | ⏳ Planned | Load/Stress | Locust, k6 |
| 6 — Security | ⏳ Planned | OWASP, pentest | ZAP, Bandit |
| 7 — Accessibility | ⏳ Planned | WCAG 2.1 | axe-playwright |
| 8 — Database | ⏳ Planned | Data integrity | Testcontainers |
| 9 — Quality | ⏳ Planned | Mutation testing | mutmut, Codecov |
| 10 — AI Testing | ⏳ Planned | LLM evaluation | DeepEval, Ollama |
| 11 — AI Agents | ⏳ Planned | Agent delegation | LangChain |
| 12 — Monitoring | ⏳ Planned | Dashboard | Grafana, Prometheus |
| 13 — Advanced | ⏳ Planned | Chaos, i18n, mobile | toxiproxy |

Full plan: [`plan/OVERVIEW.md`](plan/OVERVIEW.md)

---

## 🛠️ Dev Tools

```bash
# Lint + format
ruff check . --fix
ruff format .

# Type checking
mypy src/

# Pre-commit hooks (run on every git commit)
pre-commit install
pre-commit run --all-files
```

---

## 📦 Tech Stack (Phase 1)

| Tool | Version | Purpose |
|------|---------|---------|
| Python | 3.12 | Language |
| Playwright | 1.61 | Browser automation |
| pytest | 9.1 | Test runner |
| pytest-xdist | 3.8 | Parallel execution |
| pydantic-settings | 2.14 | Typed config |
| allure-pytest | 2.16 | Rich reports |
| ruff | 0.15 | Linter + formatter |
| mypy | 2.1 | Type checker |

---

## Agent Usage Guide Framework

This directory contains a comprehensive framework for using agents and skills following the **caveman principles** — optimizing for token efficiency, clarity, and speed.

## Files

### 📄 AGENT_USAGE_GUIDE.md
**Comprehensive user guide** for all agents and skills in the caveman style.

**Best for:**
- Learning what each agent does
- Picking the right tool for your task
- Understanding patterns and best practices
- Reference when you need to "find → build → review"

**How to use:**
- Start here if you're new to the framework
- Reference when confused about which agent to use
- Share with team members

### 📄 AGENT_INSTRUCTIONS.md
**Master instruction set** — this is the ruleset that all agents should follow.

**Best for:**
- Developers integrating agents into an AI system
- Creating system prompts for agents
- Training/fine-tuning AI models
- Understanding what makes caveman agents work

**How to use:**
- Add to your agent's system prompt
- Include in fine-tuning datasets
- Reference in internal docs
- Include in CLAUDE.md or similar memory files

### 📋 agent-config.json
**Configuration file** — metadata about all agents, skills, rules, and documentation.

**Best for:**
- Automation scripts
- IDE extensions
- Agent routers/dispatchers
- Dashboard generation
- Configuration management systems

**How to use:**
- Parse in your agent routing logic
- Generate documentation from it
- Validate user input against triggers
- Track enabled/disabled agents

## Quick Start

### I want to...

**Find code** → Use `cavecrew-investigator`
```
"Where is the handleSubmit function?"
→ Investigator returns file:line + context
```

**Fix/implement something** → Use `cavecrew-builder`
```
"Implement user auth module"
→ Builder writes/edits files, returns caveman explanation
```

**Review code quality** → Use `cavecrew-reviewer`
```
"Review this code for bugs and security issues"
→ Reviewer audits, returns line-by-line feedback
```

**Save tokens** → Use `/caveman [level]`
```
/caveman ultra
→ All responses now compressed, ~75% fewer tokens
```

**Commit messages** → Use `/caveman-commit`
```
/caveman-commit
→ Structure as Conventional Commits with terse rationale
```

**PR feedback** → Use `/caveman-review`
```
/caveman-review
→ Format as one-line comments per issue
```

### Find → Build → Review Pattern

Best practice for code changes:

```
1. You: "Bug in login form. Investigate where validation happens."
   ↓
2. Investigator: Returns file:line table
   ↓
3. You: "Builder, consolidate validation, clean up duplicates"
   ↓
4. Builder: Returns modified files
   ↓
5. You: "Reviewer, audit these changes"
   ↓
6. Reviewer: Returns line-by-line feedback
   ↓
7. Builder (or you): Fix issues, re-run reviewer
   ↓
8. Done: Integrate, test, deploy
```

**Token savings:** Each agent ~60% fewer tokens than vanilla Claude Code. Combined = 2-3× context longevity.

## Integration Guide

### For AI Agents

Add to your system prompt:

```markdown
<!-- Include AGENT_INSTRUCTIONS.md content here -->
```

Or load via context:

```python
with open("AGENT_INSTRUCTIONS.md") as f:
    system_prompt += f.read()
```

### For Teams

1. **Share the guide:**
   - Link AGENT_USAGE_GUIDE.md in Slack/Discord
   - Reference `/agent-guide` when asking for help
   - Keep a printed copy at your desk (kidding)

2. **Establish standards:**
   - Use "investigator/builder/reviewer" terminology
   - Always pass investigator results to builder
   - Always pass builder results to reviewer
   - Reference `/caveman-stats` to track savings

3. **Onboarding:**
   - New team member → read AGENT_USAGE_GUIDE.md
   - Developer → read AGENT_INSTRUCTIONS.md
   - Anything breaks → refresh from caveman repo

### For Automation

Parse `agent-config.json`:

```javascript
const config = require('./agent-config.json');

// Route user request to correct agent
function routeRequest(userMessage) {
  for (const [agentName, agentConfig] of Object.entries(config.agents)) {
    for (const trigger of agentConfig.triggers) {
      if (userMessage.includes(trigger)) {
        return agentName;
      }
    }
  }
  return 'default';
}

// Check if caveman mode enabled
function getCavemanLevel() {
  return config.framework.defaultMode; // "lite", "full", "ultra", etc.
}
```

## Rules Overview

### Caveman Drop Rules

✂️ You can drop:
- Articles (a, an, the)
- Filler words (just, really, basically, actually, simply)
- Pleasantries (sure, certainly, of course, happy to)
- Hedging qualifiers (might, could be, seems like, appears)

### Caveman **Keep** Rules

🔒 Always preserve:
- Code blocks (exact syntax, never caveman-ify)
- Error strings (verbatim, byte-exact)
- API names (exact, backticked)
- Function names (exact)
- CLI commands (exact)
- Commit keywords: feat/fix/docs/style/refactor/perf/test/chore
- Technical terms (domain language)

### Auto-Clarity Exceptions

🚨 Stop caveman for:
- Security warnings (use Normal English)
- Destructive operations (full clarity, confirm)
- Multi-step sequences where order matters
- Statements that lose meaning when compressed
- When user asks for repetition

### Language Preservation

🌍 Compress the **style**, keep the **language**:
- User writes Portuguese → reply Portuguese caveman
- User writes Spanish → reply Spanish caveman
- User writes English → reply English caveman

## Modes Explained

| Mode | Use When | Example |
|------|----------|---------|
| **lite** | You want short but readable | "Your component re-renders because of new refs. Use `useMemo`." |
| **full** | Default, balanced compression | "New object ref each render. Wrap in `useMemo`." |
| **ultra** | Maximum token savings | "Inline obj → re-render. `useMemo`." |
| **wenyan-lite** | Want classical Chinese, readable | "組件頻重繪...以 useMemo 包之。" |
| **wenyan-full** | Want full 文言文, classical | "每繪新生對象參照，故重繪；useMemo wrap。" |
| **wenyan-ultra** | Maximum classical compression | "新參照→重繪。useMemo。" |

## Troubleshooting

**Q: Which agent should I use?**
A: See "Which Agent When" table in AGENT_USAGE_GUIDE.md

**Q: Caveman mode is confusing me?**
A: Say "stop caveman" or "normal mode". Resume anytime with `/caveman`.

**Q: How much do I save?**
A: `/caveman-stats` shows session + lifetime savings + USD cost.

**Q: Can I use multiple agents at once?**
A: Yes. Investigator finds code, builder fixes it, reviewer audits. Chain them.

**Q: Does caveman reduce accuracy?**
A: No. ~75% fewer *output* tokens, 100% technical accuracy maintained. Brain stays big.

**Q: What if I need a security warning?**
A: Always use Normal English for security info. Caveman resumes after confirmation.

## References

- **Main repo:** https://github.com/JuliusBrussee/caveman
- **Full terminal agent:** https://github.com/JuliusBrussee/caveman-code
- **Memory system:** https://github.com/JuliusBrussee/cavemem
- **Build loop:** https://github.com/JuliusBrussee/cavekit
- **Fine-tuned model:** https://github.com/JuliusBrussee/finetune-caveman

## What's Next?

1. **Read:** Start with AGENT_USAGE_GUIDE.md
2. **Apply:** Try `/caveman` or call an agent
3. **Chain:** Use Find → Build → Review for next major refactor
4. **Measure:** Run `/caveman-stats` to see token savings
5. **Share:** Show your team the results

---

**TL;DR:** Use investigators to find, builders to fix, reviewers to verify. Use caveman to compress. Save tokens. Stay in flow. Brain still big. Mouth just small. ⛏
