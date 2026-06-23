---
name: agent-usage-guide
description: >
  Complete reference for all agents and skills. Covers cavecrew-investigator,
  cavecrew-builder, cavecrew-reviewer, and all caveman skills. Trigger:
  /agent-guide, "agent help", "how to use agents", "tell me about agents".
---

# Agent Usage Guide — Comprehensive Reference

Brief, caveman-style instructions for all agents and skills. Technical accuracy. No fluff.

## AGENTS (Specialized Workers)

Agents = spawned subprocesses. Each do one job well. Different tools. Faster than main thread context.

### cavecrew-investigator

**Job:** Find + locate. Read-only. Never edit.

**Use when:**
- "Where is X defined?"
- "What calls Y?"
- "List all uses of Z"
- "Map this codebase"
- "Find all imports of module"

**Output:** File:line table with symbols. Caveman-ultra (super terse).

**Tools:** Read, Grep, Bash (git log, git grep, find).

**What it won't do:** Fix, suggest changes, design architecture.

**Spawn it:** Main thread say "Investigate [question]" or direct spawn with query.

**Example:**
```
Q: "where handleSubmit defined in codebase?"

Defs:
- src/forms/submit-handler.js:42 - main impl
- src/hooks/useSubmit.ts:100 - wrapper

Callers:
- src/pages/Login.tsx:15,33
- src/pages/Register.tsx:22

2 defs, 2 callers.
```

---

### cavecrew-builder

**Job:** Build + fix + code. Write files. Edit existing. Design solutions.

**Use when:**
- investigator found issue, now fix it
- "Implement feature X"
- "Refactor this module"
- "Write unit test for Y"
- "Optimize Z"

**Output:** Modified/new files. Caveman-compressed explanations. Code blocks exact (no caveman).

**Tools:** File read/write/edit, terminal access. Full codebase context.

**What it won't do:** Long design docs. Starts build → provides small, focused tasks.

**Spawn it:** Main thread say "Build [task]" or after investigator finds root cause.

**Pattern:** Investigator → Builder → Reviewer.

---

### cavecrew-reviewer

**Job:** Review + audit. Junior → Senior conversion. Adversarial check.

**Use when:**
- "Review this code for bugs"
- "Security audit Z"
- "Check performance"
- "Validate architecture"
- Builder finished, needs final pass

**Output:** Line-by-line comments. `L42: 🔴 bug: null check missing. Add guard.` Format caveman-ultra.

**Tools:** Read, Grep, patterns. Read-only (reports, not edits).

**What it won't do:** Fix directly. Pass → suggests fixes.

**Spawn it:** "Review X for [concern]" or after builder completes.

---

## SKILLS (Persistent Modes)

Skills = agent behavior modifications. Activate once, persist until you deactivate. Apply to ALL agent responses.

### /caveman [lite|full|ultra|wenyan-lite|wenyan-full|wenyan-ultra]

**What:** Ultra-compressed communication. Drop filler, keep substance.

**Levels:**
- **lite** — Drop filler, keep sentence structure. Professional but tight.
- **full** — Default. Drop articles/filler/hedging. Fragments OK. Short synonyms.
- **ultra** — Max compression. Abbreviate prose words only (auth/config/req/res). Never abbreviate code/function names.
- **wenyan-lite** — Classical Chinese, light compression.
- **wenyan-full** — Full 文言文. 80-90% reduction. Classical patterns.
- **wenyan-ultra** — Extreme classical. Maximum compression.

**Activate:** `/caveman` or `/caveman ultra`

**Deactivate:** "stop caveman" or "normal mode"

**Persist until:** Changed, session end, or deactivated.

**Saves:** ~65% output tokens (range 22-87% depending on task).

**Example (React re-render bug):**
- Normal: "Your component re-renders because you create new object refs each cycle..."
- Full: "New object ref each render. Inline object prop = new ref. Wrap in `useMemo`."
- Ultra: "Inline obj prop → new ref → re-render. `useMemo`."

---

### /caveman-commit

**What:** Commit message generator. Conventional Commits format. ≤50 char subject. Why > what.

**Activate:** `/caveman-commit`

**Output format:**
```
feat: add user auth module (≤50 chars)

- Point 1 (terse reason)
- Point 2 (impact)
```

**Keys:** Subject short. Why matter. No "change X to Y" style, state impact.

---

### /caveman-review

**What:** One-line PR comments. Terse, actionable feedback.

**Activate:** `/caveman-review`

**Output format:**
```
L42: 🔴 bug: null user unchecked. Add guard.
L88: 🟡 perf: O(n²) loop. Consider Map or Set.
L120: 🟢 OK: test coverage good.
```

**Logic:** Line number, severity emoji, issue type, fix hint.

---

### /caveman-compress

**What:** Rewrite .md files to caveman prose. Input memory files, config docs, project notes.

**Use:** `/caveman-compress <file>`

**Saves:** ~46% input tokens every session (real-world data).

**Example:**
- Original: "In this document, we will discuss the various ways in which you might approach handling user authentication..."
- Compressed: "Auth approaches: sessions, JWT, OAuth. Pick one-based on scope + latency budget."

**Preserves:** Code blocks, URLs, paths, technical terms — byte-exact. Only style compress.

---

### /caveman-stats

**What:** Token usage report. Session + lifetime savings. USD cost.

**Activate:** `/caveman-stats` or `/caveman-stats --share` (tweetable)

**Output:**
```
Session tokens saved: 4,200 (43%)
Lifetime saved: 89,450 tokens (~$0.45 at GPT-4 rates)
Badge: [CAVEMAN] ⛏ 12.4k
```

---

### /caveman-help

**What:** Quick reference card. This you reading right now, but one-liner format.

**Activate:** `/caveman-help`

---

## PATTERNS & BEST PRACTICE

### Pattern: Find → Build → Review

**Flow:**
1. Main thread → `cavecrew-investigator` — "Where root cause?"
2. Investigator return → Pass to `cavecrew-builder` — "Fix it"
3. Builder returns → `cavecrew-reviewer` — "Any bugs?"
4. All done → Return main

**Tokens:** Each agent ~60% fewer than vanilla. Combine = 2-3x main context longevity.

---

### When to Use Which

| You need | Use |
|----------|-----|
| Code location | cavecrew-investigator |
| Implement/fix | cavecrew-builder |
| Quality review | cavecrew-reviewer |
| Token savings | /caveman |
| Commit messages | /caveman-commit |
| PR feedback | /caveman-review |
| Memory compress | /caveman-compress |
| Cost report | /caveman-stats |

---

### Agent Priority (Caveman Mode Precedence)

If `/caveman ultra` active:
1. **Security warnings** → Normal English (not caveman). Resume after.
2. **Destructive operations** → Full clarity (not caveman). Confirm.
3. **Ambiguity risk** → Normal (e.g., "delete user ID 42" could mean column or record). Resume.
4. **Code blocks** → Exact. Never caveman code syntax.
5. **Error strings** → Verbatim.

---

## TRIGGER KEYWORDS

**Investigator:**
- "Where is X defined?"
- "What calls Y?"
- "Find all uses of Z"
- "Map codebase"
- "List imports of module"

**Builder:**
- "Implement X"
- "Fix bug (after investigator)"
- "Refactor Y"
- "Write test"
- "Optimize Z"

**Reviewer:**
- "Review for bugs"
- "Security audit"
- "Performance check"
- "Architecture review"

**Caveman mode:**
- "Talk like caveman"
- "Use caveman"
- "Less tokens"
- "Be brief"
- `/caveman [level]`

**Caveman commit:**
- `/caveman-commit`
- "Commit message"

**Caveman review:**
- `/caveman-review`
- "Review code line-by-line"

---

## CONFIGURATION

### Default Caveman Level

Set environment variable (highest priority):
```bash
export CAVEMAN_DEFAULT_MODE=ultra
```

Or config file `~/.config/caveman/config.json`:
```json
{ "defaultMode": "lite" }
```

Resolution: env var > config > `full`.

---

## ANTI-PATTERNS (Don't)

❌ Ask investigator to fix — tell it "Builder time"
❌ Ask builder for location query — use investigator
❌ Caveman mode for security warnings — always use normal English
❌ Mix caveman compressed code with real code (confuse reader)
❌ Invent abbreviations reader can't decode

## LANGUAGE

All agents preserve your language. Write Portuguese → reply Portuguese caveman. English → English caveman. French → French caveman.

Technical terms, code, API names, commit keywords (feat/fix), error strings — always exact, never translate/caveman-ify.

---

## EXAMPLES

### Find + Fix + Review Pattern

**Q:** "Bug in login form. Find where form submit validate user."

1. **Investigator spawned:** "Where is validation?"
   ```
   Defs:
   - src/auth/validate.ts:42 — userExists check
   - src/forms/Login.tsx:88 — inline validation

   Callers:
   - src/pages/Login.tsx:15

   2 defs, 1 caller.
   ```

2. **Builder spawned:** "Consolidate. Leverage validator at ts:42. Remove dup at Login.tsx:88."
   ```
   Edit: src/forms/Login.tsx — remove lines 88-95 (validation), import from validate.ts
   Edit: src/auth/validate.ts — add email format check to userExists
   New: src/__tests__/auth.validate.test.ts — test harness
   ```

3. **Reviewer spawned:** "Audit changes for bugs/perf/types."
   ```
   L14: 🔴 import missing: validateUser not exported. Add to validate.ts exports.
   L25: 🟡 perf: validateUser called twice (submit + change). Debounce?
   L88: 🟢 types: userExists typed correct (Promise<boolean>).
   1 blocker, 1 warning, coverage OK.
   ```

**Main thread:** "Fix import, add debounce, re-run tests. Done."

---

## QUICK START

1. **Know what you need:**
   - Code location? → `cavecrew-investigator`
   - Code change? → `cavecrew-builder`
   - Quality check? → `cavecrew-reviewer`
   - Fewer tokens? → `/caveman [ultra]`

2. **Spawn or activate:**
   - "Investigate X" → spawns investigator
   - "Build X" → spawns builder
   - "Review X" → spawns reviewer
   - "/caveman" → activates mode (all responses caveman)

3. **Chain:** Investigator → Builder → Reviewer for full cycle.

4. **Deactivate caveman:** "stop caveman" or "normal mode" (toggles off, keep all agents live).

---

## HELP & DOCS

Full documentation: https://github.com/JuliusBrussee/caveman

See also: [caveman-code](https://github.com/JuliusBrussee/caveman-code) (full terminal agent).

Report issues: https://github.com/JuliusBrussee/caveman/issues

---

**Why?** Caveman = ~75% fewer output tokens while keeping 100% technical accuracy. Spend less on tokens, fit more in context window, keep session longer, stay in flow.

**Brain still big. Mouth just small. ⛏**
