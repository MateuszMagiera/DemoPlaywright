# Caveman Agent Framework — Complete Bundle

This directory contains a complete, ready-to-use agent framework based on the caveman principles from https://github.com/JuliusBrussee/caveman.

## 📦 What's Inside

### Core Documentation Files

1. **README.md** (← Start here!)
   - Overview of the framework
   - Quick start guide
   - Integration instructions for teams
   - Troubleshooting FAQ

2. **AGENT_USAGE_GUIDE.md** (← For users)
   - Comprehensive guide to all agents and skills
   - When to use each agent
   - Pattern walkthroughs
   - Examples and real-world usage

3. **AGENT_INSTRUCTIONS.md** (← For developers)
   - Master instruction set for all agents
   - Rules and principles
   - Language preservation
   - Auto-clarity exceptions
   - **Add this to your system prompt**

4. **CHEATSHEET.md** (← Quick reference)
   - One-page summary
   - All commands and triggers
   - Quick decision matrix
   - Print and tape to monitor

5. **IMPLEMENTATION_GUIDE.md** (← For engineers)
   - Step-by-step integration instructions
   - Python code examples
   - Architecture diagrams
   - Complete working example

### Configuration File

6. **agent-config.json**
   - Machine-readable configuration
   - All agent definitions
   - Skill metadata
   - Rules and patterns
   - Use in automation/routing logic

---

## 🚀 Quick Start (5 Minutes)

### For Users

1. **Read:** README.md (2 min)
2. **Try:** Run `/caveman` in any conversation (1 min)
3. **Explore:** Check CHEATSHEET.md (2 min)

### For Developers

1. **Read:** README.md (2 min)
2. **Study:** IMPLEMENTATION_GUIDE.md (10 min)
3. **Integrate:** Add AGENT_INSTRUCTIONS.md to system prompt (5 min)
4. **Test:** Use agent-config.json in router (15 min)

### For Product Managers

1. **Read:** README.md (2 min)
2. **Review:** AGENT_USAGE_GUIDE.md sections on "Pattern: Find → Build → Review" (5 min)
3. **Estimate:** ~60-75% token savings per cycle (check benchmarks in caveman repo)

---

## 🎯 How to Use Each File

### README.md
**Contains:**
- Framework overview
- Integration guides (for developers/teams/automation)
- Usage examples
- Troubleshooting

**Read when:**
- You're new to the framework
- You need integration instructions
- You have questions

**Action:** Start here. Links to other files.

---

### AGENT_USAGE_GUIDE.md
**Contains:**
- Complete reference for all agents and skills
- When to use each agent
- Output format examples
- Decision matrix (which tool for which task)
- Pattern walkthrough (find → build → review)
- Language rules
- Configuration instructions

**Read when:**
- You want to use an agent or skill
- You're not sure which tool to pick
- You need detailed examples

**Action:** Bookmark this. Reference constantly.

---

### AGENT_INSTRUCTIONS.md
**Contains:**
- Master ruleset for all agents
- What to drop in caveman mode
- What to always preserve
- Precedence rules (when not to use caveman)
- Language preservation rules
- Anti-patterns

**Read when:**
- You're a developer integrating the framework
- You're training/fine-tuning models
- You need to understand the principles

**Action:** Add entire content to your agent's system prompt. Include in CLAUDE.md.

---

### CHEATSHEET.md
**Contains:**
- One-page summary of all agents and skills
- Quick decision matrix
- Commands and triggers
- Rules overview
- Don't/Do lists

**Read when:**
- You need a quick reminder
- You forgot the syntax
- You need to explain to someone else

**Action:** Print this. Tape it to your monitor. Reference daily.

---

### IMPLEMENTATION_GUIDE.md
**Contains:**
- Step-by-step integration instructions
- Architecture diagram
- Python code examples:
  - Skill router
  - Agent router
  - Caveman formatter
  - Find → Build → Review chain
  - Stats tracker
  - Complete working example
- Deployment checklist

**Read when:**
- You're building an agent system
- You need code examples
- You're integrating caveman into existing code

**Action:** Follow steps 1-7. Copy code examples. Test against CHEATSHEET.md examples.

---

### agent-config.json
**Contains:**
- Machine-readable definitions of all agents
- Trigger keywords for each agent
- Skill metadata
- Rules in JSON format
- Documentation links

**Read when:**
- You're building automation/routing logic
- You need to generate documentation
- You need to validate user input

**Usage example:**
```python
import json
config = json.load(open('agent-config.json'))
triggers = config['agents']['cavecrew-investigator']['triggers']
```

---

## 🔄 Typical Workflows

### Workflow 1: Using Agents (End User)

```
1. Read: README.md + CHEATSHEET.md (5 min)
2. Try: "Find where user validation happens"
   → Investigator returns file:line table
3. Ask: "Builder, consolidate this validation code"
   → Builder returns modified files
4. Ask: "Reviewer, audit these changes"
   → Reviewer returns line-by-line feedback
5. Activate: "/caveman ultra"
   → All responses now ~75% fewer tokens
6. Check: "/caveman-stats"
   → See how many tokens saved
```

### Workflow 2: Implementing the Framework (Developer)

```
1. Read: README.md + IMPLEMENTATION_GUIDE.md (15 min)
2. Add: AGENT_INSTRUCTIONS.md to system prompt
3. Parse: agent-config.json in your router
4. Code: Implement routers (skill + agent)
5. Code: Implement caveman formatter
6. Test: Run against CHEATSHEET.md commands
7. Deploy: Load into production agent
8. Monitor: Track with caveman-stats
```

### Workflow 3: Team Onboarding (Manager)

```
1. Share: Link to README.md in Slack
2. Suggest: Read AGENT_USAGE_GUIDE.md
3. Print: CHEATSHEET.md for each desk
4. Establish: Standard terminology (investigator, builder, reviewer)
5. Measure: Run /caveman-stats --share to show ROI
6. Encourage: Use Find → Build → Review pattern for code changes
7. Monitor: Track team's token-saved stats over time
```

---

## 📊 Files at a Glance

| File | Size | Read Time | Purpose | Audience |
|------|------|-----------|---------|----------|
| README.md | ~4KB | 5 min | Overview + integration | Everyone |
| AGENT_USAGE_GUIDE.md | ~8KB | 10 min | Complete user reference | Users + developers |
| AGENT_INSTRUCTIONS.md | ~12KB | 15 min | Master rules | Developers + AI systems |
| CHEATSHEET.md | ~2KB | 2 min | Quick reference | Everyone |
| IMPLEMENTATION_GUIDE.md | ~10KB | 20 min | Code integration | Developers |
| agent-config.json | ~4KB | N/A | Machine-readable config | Automation/tools |

**Total:** ~40KB of documentation and configuration. Print-friendly. No external dependencies.

---

## 🎓 Learning Paths

### Path 1: "I want to use this NOW" (15 minutes)
1. Skim README.md (2 min)
2. Read CHEATSHEET.md (2 min)
3. Try: `/caveman` command in your agent (1 min)
4. Try: "Find where handleSubmit is defined" (5 min)
5. Try: "Builder, refactor this code" (5 min)

### Path 2: "I want to understand everything" (30 minutes)
1. Read README.md (5 min)
2. Read AGENT_USAGE_GUIDE.md (10 min)
3. Skim AGENT_INSTRUCTIONS.md (5 min)
4. Study CHEATSHEET.md (2 min)
5. Bookmark IMPLEMENTATION_GUIDE.md for later (N/A)

### Path 3: "I'm implementing this" (60 minutes)
1. Read README.md (5 min)
2. Study IMPLEMENTATION_GUIDE.md (20 min)
3. Read AGENT_INSTRUCTIONS.md carefully (15 min)
4. Code: Implement routers + formatter (15 min)
5. Test: Run against CHEATSHEET.md examples (5 min)

### Path 4: "I'm training a model on this" (45 minutes)
1. Read AGENT_INSTRUCTIONS.md carefully (20 min)
2. Review IMPLEMENTATION_GUIDE.md code examples (15 min)
3. Study CHEATSHEET.md patterns (5 min)
4. Create training pairs from examples (5 min)

---

## ✅ Implementation Checklist

- [ ] Read README.md
- [ ] Understand agents (investigator/builder/reviewer)
- [ ] Understand skills (caveman modes + commands)
- [ ] Add AGENT_INSTRUCTIONS.md to system prompt
- [ ] Implement skill router (route /caveman, /caveman-commit, etc.)
- [ ] Implement agent router (detect investigator/builder/reviewer triggers)
- [ ] Implement caveman formatter (drop rules, abbreviations, auto-clarity)
- [ ] Implement Find → Build → Review chain
- [ ] Test all commands from CHEATSHEET.md
- [ ] Track stats with caveman-stats
- [ ] Deploy to production
- [ ] Share framework with team
- [ ] Get feedback, iterate

---

## 🔗 Related Resources

**Official caveman repository:**
https://github.com/JuliusBrussee/caveman

**Related projects:**
- caveman-code (full terminal agent): https://github.com/JuliusBrussee/caveman-code
- cavemem (cross-agent memory): https://github.com/JuliusBrussee/cavemem
- cavekit (spec-driven build loop): https://github.com/JuliusBrussee/cavekit
- cavegemma (fine-tuned model): https://github.com/JuliusBrussee/finetune-caveman

**Benchmark data:**
See original caveman repo for token usage benchmarks (~65% average output reduction across diverse tasks)

---

## 💡 Pro Tips

1. **Print CHEATSHEET.md** — Have it at your desk. Refer to it constantly.

2. **Start with Find → Build → Review** — Use the full chain on your next code change. See the token savings firsthand.

3. **Use /caveman-stats** — Run this weekly. Track your token savings. Share with team for motivation.

4. **Preserve language** — If you write Spanish, your agent replies Spanish caveman. Same for Portuguese, French, etc.

5. **Code blocks are sacred** — API names, function names, error strings, CLI commands — never caveman-ify these.

6. **Auto-clarity** — Security warnings? Destructive operations? Use Normal English. The caveman framework knows when to speak clearly.

7. **Chain agents** — Don't ask builder where code is. Use investigator first, then builder. Different tools.

---

## ❓ FAQ

**Q: Do I lose accuracy with caveman mode?**
A: No. ~75% fewer output tokens, 100% technical accuracy. Brain stays big, mouth gets small.

**Q: Can I use multiple agents at once?**
A: Yes! Use investigator to find code, builder to fix it, reviewer to audit. Chain them.

**Q: What if caveman mode confuses me?**
A: Say "stop caveman" or "normal mode". Resume anytime with `/caveman`.

**Q: Does this work with my existing agent?**
A: Yes. Add AGENT_INSTRUCTIONS.md to system prompt. Parse agent-config.json for routers.

**Q: How much can I save?**
A: Average 65% output token reduction. Range 22-87% depending on task type.

**Q: Can I use this with Claude Code, Cursor, Gemini, etc.?**
A: Yes. Works with any agent. Add instructions to system prompt.

**Q: Is there a fine-tuned model?**
A: Yes, cavegemma (Gemma 4 31B fine-tuned on caveman pairs). See caveman repo docs.

---

## 🤝 Contributing

Want to improve this framework? See the original repository:
https://github.com/JuliusBrussee/caveman/blob/main/CONTRIBUTING.md

---

## 📜 License

This framework is based on caveman, which is MIT licensed (free).

---

## 🎩 Attribution

**Original caveman concept:** Julius Brussee
https://github.com/JuliusBrussee

**This implementation:** Adapted for DemoPlaywright project
`C:\Users\pc\PycharmProjects\DemoPlaywright`

---

**Get started:**
1. Open README.md
2. Pick your role (user/developer/team lead)
3. Follow the learning path
4. Use the framework
5. Save tokens
6. Stay sharp

⛏ **Brain big. Mouth small. Context long. Vibes good.**
