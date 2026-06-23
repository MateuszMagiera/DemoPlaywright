# Agent Usage Guide Framework

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
