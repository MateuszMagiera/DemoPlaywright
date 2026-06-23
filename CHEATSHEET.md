# Caveman Agent Framework — Cheat Sheet

## 🪨 AGENTS (Specialists)

| Agent | Job | Trigger | Output |
|-------|-----|---------|--------|
| **investigator** | Find code | "Where is X?" | file:line table |
| **builder** | Build + fix | "Implement Y" | modified files |
| **reviewer** | Audit code | "Review Z" | L<line>: emoji issue |

## 📊 SKILLS (Modes)

| Skill | Do | Trigger |
|-------|----|----|
| **caveman** | Compress output | `/caveman [lite\|full\|ultra]` |
| **caveman-commit** | Commit message | `/caveman-commit` |
| **caveman-review** | PR comments | `/caveman-review` |
| **caveman-compress** | Shrink .md files | `/caveman-compress <file>` |
| **caveman-stats** | Token savings | `/caveman-stats` |
| **caveman-help** | Quick ref | `/caveman-help` |

## 🔄 PATTERN: Find → Build → Review

```
User: "Bug in login. Find it."
  ↓
Investigator: file:line + context
  ↓
User: "Build: fix the issue"
  ↓
Builder: modified files
  ↓
User: "Review: audit changes"
  ↓
Reviewer: line-by-line feedback
  ↓
Done
```

## ⚡ CAVEMAN LEVELS

**lite** — Professional tight (keep articles, drop filler)
**full** — Default (drop articles + filler, fragments OK)
**ultra** — Max compression (abbreviate prose, keep code exact)
**wenyan-lite** — Classical Chinese light
**wenyan-full** — Full 文言文 classical
**wenyan-ultra** — Maximum classical terse

## ✂️ CAVEMAN DROP

- a / an / the
- just, really, basically, actually, simply
- sure, certainly, of course, happy to
- might, could be, seems, appears

## 🔒 CAVEMAN KEEP

- Code blocks (exact)
- Error strings (verbatim)
- API names (backticked)
- Function names (exact)
- CLI commands (exact)
- feat / fix / docs / style / refactor / perf / test / chore
- Technical terms

## 🚨 USE NORMAL ENGLISH

- Security warnings
- Destructive operations
- Complex multi-step sequences
- Ambiguous logic (order matters)
- When user asks to clarify

## 📋 PICK RIGHT TOOL

| Goal | Use |
|------|-----|
| "Where is X?" | investigator |
| "Fix Y" | builder |
| "Audit Z" | reviewer |
| "Fewer tokens" | caveman |
| "Commit" | caveman-commit |
| "PR comment" | caveman-review |
| "Shrink notes" | caveman-compress |
| "Cost report" | caveman-stats |

## ⌨️ QUICK COMMANDS

```
Find code:
"Where is handleSubmit defined?"

Fix code:
"Implement user authentication module"

Review code:
"Security audit this login form"

Save tokens:
"/caveman ultra"

Commit message:
"/caveman-commit"

PR feedback:
"/caveman-review"

Token report:
"/caveman-stats"

Turn off caveman:
"stop caveman" or "normal mode"

Help:
"/caveman-help" or "/agent-guide"
```

## 📊 SAVINGS

| Task | Normal | Caveman | Saved |
|------|--------|---------|-------|
| React re-render | 1180 | 159 | 87% |
| Auth bug | 704 | 121 | 83% |
| DB setup | 2347 | 380 | 84% |
| **Average** | 1214 | 294 | **65%** |

## 🚫 DON'T

❌ Ask investigator to fix
❌ Ask builder to find code
❌ Caveman on security warnings
❌ Caveman-ify code syntax
❌ Invent abbreviations
❌ Self-reference the mode

## ✅ DO

✅ Ask investigator to locate
✅ Ask builder to implement
✅ Use Normal English for security
✅ Keep code blocks exact
✅ Use common acronyms only (DB/API/HTTP)
✅ Just do caveman, don't announce it

## 📚 LANGUAGE

User Portuguese → reply Portuguese caveman
User Spanish → reply Spanish caveman
User English → reply English caveman
**Preserve domain language + code always**

## 🔗 LINKS

- Docs: https://github.com/JuliusBrussee/caveman
- Full agent: https://github.com/JuliusBrussee/caveman-code
- Memory: https://github.com/JuliusBrussee/cavemem
- Build: https://github.com/JuliusBrussee/cavekit

## 🎯 ONE-LINE RULES

**Investigator:** Find + report. Stop.
**Builder:** Build + explain. Code exact.
**Reviewer:** Audit + report. No edits.
**Caveman:** Drop fluff. Keep substance. ~75% fewer tokens.

---

**Print this. Tape to monitor. Use every day.**

⛏ Brain big. Mouth small. Context long. Tokens cheap. Vibes good.
