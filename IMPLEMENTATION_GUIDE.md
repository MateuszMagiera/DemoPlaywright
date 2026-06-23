# Implementation Guide — Caveman Agent Framework

For developers integrating the caveman agent framework into their systems.

## Overview

The framework consists of:

1. **Three specialist agents:** investigator (find), builder (build), reviewer (review)
2. **Six skills:** caveman (output compression), caveman-commit, caveman-review, caveman-compress, caveman-stats, caveman-help
3. **Master instructions:** In AGENT_INSTRUCTIONS.md (add to system prompts)
4. **Configuration:** agent-config.json (metadata + rules)

## Architecture

```
┌──────────────────────────────────┐
│      User Request                │
└──────────────────────────────────┘
           ↓
┌──────────────────────────────────┐
│   Skill Router                   │  ← Check if /caveman, /agent-guide, etc.
│   - Parse mode (lite/full/ultra) │  ← Apply caveman rules to output
│   - Apply language pref          │  ← Preserve user's language
└──────────────────────────────────┘
           ↓
┌──────────────────────────────────┐
│   Agent Router                   │  ← Route to investigator/builder/reviewer
│   - Check triggers               │    or route to main agent
│   - Select tools                 │
│   - Apply mode constraints       │
└──────────────────────────────────┘
           ↓
┌──────────────────────────────────┐
│   Specialist Agent               │  ← Run investigator/builder/reviewer
│   - Execute specialized task     │    (or main agent with skill applied)
│   - Apply caveman rules          │
│   - Auto-clarity exceptions      │
└──────────────────────────────────┘
           ↓
┌──────────────────────────────────┐
│   Output Formatter               │  ← Format per agent specs
│   - Apply caveman level          │  ← Apply auto-clarity rules
│   - Preserve code/errors         │  ← Preserve language
└──────────────────────────────────┘
           ↓
┌──────────────────────────────────┐
│      User Response               │
└──────────────────────────────────┘
```

## Step 1: Load Configuration

Load the JSON config:

```python
import json

with open('agent-config.json') as f:
    config = json.load(f)

# Access agents, skills, rules
agents = config['agents']
skills = config['skills']
rules = config['rules']
```

## Step 2: Implement Skill Router

Detect which skill user is requesting:

```python
def route_skill(user_message: str) -> tuple[str, dict]:
    """Returns (skill_name, skill_config) or (None, {}) if no skill"""

    message_lower = user_message.lower()

    # Check caveman modes
    if '/caveman' in message_lower:
        level = 'full'  # default
        if 'lite' in message_lower:
            level = 'lite'
        elif 'ultra' in message_lower:
            level = 'ultra'
        elif 'wenyan' in message_lower:
            if 'ultra' in message_lower:
                level = 'wenyan-ultra'
            elif 'full' in message_lower or message_lower.endswith('wenyan'):
                level = 'wenyan-full'
            else:
                level = 'wenyan-lite'

        return ('caveman', {'level': level})

    # Check other skills
    if '/caveman-commit' in message_lower or 'commit message' in message_lower:
        return ('caveman-commit', {})

    if '/caveman-review' in message_lower or ('review' in message_lower and 'pr' in message_lower):
        return ('caveman-review', {})

    if '/caveman-compress' in message_lower or 'compress' in message_lower:
        # Extract filename
        import re
        match = re.search(r'compress\s+(\S+)', message_lower)
        filename = match.group(1) if match else None
        return ('caveman-compress', {'file': filename})

    if '/caveman-stats' in message_lower or 'token' in message_lower and 'stats' in message_lower:
        share = '--share' in message_lower
        return ('caveman-stats', {'share': share})

    if '/caveman-help' in message_lower or 'caveman help' in message_lower:
        return ('caveman-help', {})

    return (None, {})
```

## Step 3: Implement Agent Router

Route to specialist agents:

```python
def route_agent(user_message: str) -> tuple[str, dict]:
    """Returns (agent_name, agent_config) or (None, {}) if no agent"""

    message_lower = user_message.lower()

    # Investigator triggers
    investigator_triggers = [
        'where is', 'where are', 'find', 'locate', 'search',
        'what calls', 'what uses', 'usage of', 'references',
        'map', 'codebase', 'imports', 'definition'
    ]

    if any(trigger in message_lower for trigger in investigator_triggers):
        return ('cavecrew-investigator', config['agents']['cavecrew-investigator'])

    # Builder triggers
    builder_triggers = [
        'implement', 'build', 'create', 'fix', 'refactor',
        'write', 'design', 'optimize', 'edit', 'modify'
    ]

    if any(trigger in message_lower for trigger in builder_triggers):
        return ('cavecrew-builder', config['agents']['cavecrew-builder'])

    # Reviewer triggers
    reviewer_triggers = [
        'review', 'audit', 'check', 'verify', 'inspect',
        'security', 'performance', 'quality', 'test'
    ]

    if any(trigger in message_lower for trigger in reviewer_triggers):
        # But if it says "build" first, might be builder with "then review"
        if 'build' in message_lower and message_lower.index('build') < message_lower.index('review'):
            return (None, {})  # Let builder handle, it'll spawn reviewer
        return ('cavecrew-reviewer', config['agents']['cavecrew-reviewer'])

    return (None, {})
```

## Step 4: Implement Caveman Output Formatter

Apply caveman rules to response:

```python
def apply_caveman(text: str, level: str = 'full', auto_clarity: bool = True) -> str:
    """Apply caveman compression rules to text"""

    # Auto-clarity: don't caveman certain situations
    if auto_clarity:
        if any(word in text.lower() for word in ['security', 'delete', 'drop table', 'warning']):
            return text  # Keep normal English

    drop_words = {
        'lite': set(),  # lite doesn't drop articles
        'full': {'a', 'an', 'the', 'just', 'really', 'basically', 'actually', 'simply',
                'sure', 'certainly', 'of course', 'happy to'},
        'ultra': {'a', 'an', 'the', 'just', 'really', 'basically', 'actually', 'simply',
                 'sure', 'certainly', 'of course', 'happy to', 'might', 'could', 'seems'}
    }

    if level == 'lite':
        # Drop filler only, keep articles + sentence structure
        words_to_drop = drop_words['lite']
    elif level == 'full':
        # Drop articles + filler, fragments OK
        words_to_drop = drop_words['full']
    elif level == 'ultra':
        # Max compression, abbreviate prose (but never code)
        words_to_drop = drop_words['ultra']
        # Add prose abbreviations (DB, auth, config, req, res, impl, fn)
        # but preserve code symbols (backticked items)
        text = abbreviate_prose_only(text)

    # Drop words from sentences
    import re
    for word in words_to_drop:
        # Replace " word " with " " but preserve exact syntax
        text = re.sub(r'\s+' + re.escape(word) + r'\s+', ' ', text, flags=re.IGNORECASE)

    return text.strip()


def abbreviate_prose_only(text: str) -> str:
    """Abbreviate prose words only in ultra mode, never code symbols"""

    # Don't abbreviate if in backticks (code/function names)
    code_pattern = r'`[^`]+`'
    code_blocks = re.findall(code_pattern, text)

    abbreviations = {
        'database': 'DB',
        'authentication': 'auth',
        'configuration': 'config',
        'request': 'req',
        'response': 'res',
        'implementation': 'impl',
        'function': 'fn',
    }

    for full, abbrev in abbreviations.items():
        # Only outside code blocks
        text = re.sub(r'\b' + full + r'\b(?!`)', abbrev, text, flags=re.IGNORECASE)

    return text
```

## Step 5: Add to System Prompt

For Claude Code or other agents, prepend AGENT_INSTRUCTIONS.md:

```python
def build_system_prompt(base_prompt: str, include_agents: bool = True) -> str:
    """Build system prompt with optional agent instructions"""

    if include_agents:
        with open('AGENT_INSTRUCTIONS.md') as f:
            agent_instructions = f.read()
        return agent_instructions + '\n\n---\n\n' + base_prompt

    return base_prompt
```

## Step 6: Implement Find → Build → Review Chain

```python
class AgentChain:
    def __init__(self, config: dict):
        self.config = config
        self.current_agent = None
        self.history = []

    def start_investigation(self, query: str):
        """Spawn investigator"""
        self.current_agent = 'investigator'
        result = run_agent('cavecrew-investigator', query)
        self.history.append({
            'agent': 'investigator',
            'query': query,
            'result': result
        })
        return result

    def build_from_investigation(self, fix_instruction: str):
        """Pass investigator result to builder"""
        if not self.history or self.history[-1]['agent'] != 'investigator':
            raise ValueError("Run investigation first")

        investigation = self.history[-1]['result']
        combined_input = f"{investigation}\n\nTask: {fix_instruction}"

        self.current_agent = 'builder'
        result = run_agent('cavecrew-builder', combined_input)
        self.history.append({
            'agent': 'builder',
            'query': fix_instruction,
            'result': result
        })
        return result

    def review_builder_output(self):
        """Pass builder result to reviewer"""
        if not self.history or self.history[-1]['agent'] != 'builder':
            raise ValueError("Run builder first")

        changes = self.history[-1]['result']

        self.current_agent = 'reviewer'
        result = run_agent('cavecrew-reviewer',
                          f"Review these changes for bugs/security/performance:\n{changes}")
        self.history.append({
            'agent': 'reviewer',
            'query': 'audit',
            'result': result
        })
        return result

    def full_cycle(self, investigation_query: str, fix_instruction: str):
        """Run full find → build → review cycle"""
        inv = self.start_investigation(investigation_query)
        build = self.build_from_investigation(fix_instruction)
        review = self.review_builder_output()

        return {
            'investigation': inv,
            'changes': build,
            'audit': review
        }

# Usage
chain = AgentChain(config)
results = chain.full_cycle(
    investigation_query="Where is user validation done?",
    fix_instruction="Consolidate validation, remove duplicates"
)
```

## Step 7: Track Caveman Stats

```python
class CavemanStats:
    def __init__(self):
        self.session_tokens_saved = 0
        self.lifetime_tokens_saved = 0
        self.session_start = datetime.now()

    def record_call(self, caveman_level: str, normal_tokens: int, caveman_tokens: int):
        """Record a caveman compression"""
        saved = normal_tokens - caveman_tokens
        self.session_tokens_saved += saved
        self.lifetime_tokens_saved += saved

    def get_report(self, share: bool = False):
        """Generate stats report"""
        pct_saved = (self.session_tokens_saved / 1000) * 100 if self.session_tokens_saved > 0 else 0

        report = f"""
Session tokens saved: {self.session_tokens_saved} (~{pct_saved:.0f}%)
Lifetime saved: {self.lifetime_tokens_saved} tokens (~${self.lifetime_tokens_saved * 0.00003:.2f} at GPT-4 rates)
Badge: [CAVEMAN] ⛏ {self.lifetime_tokens_saved}
        """

        if share:
            # Tweetable version
            return f"Just saved {self.session_tokens_saved} tokens with caveman agents! ⛏ Brain big, mouth small. https://github.com/JuliusBrussee/caveman"

        return report

# Usage
stats = CavemanStats()
stats.record_call('full', 1000, 300)  # Saved 700 tokens
print(stats.get_report())
```

## Complete Integration Example

```python
from datetime import datetime
import json
import re

# Load config
with open('agent-config.json') as f:
    config = json.load(f)

# Define routers, formatters, etc. (from steps above)

class CavemanAgentSystem:
    def __init__(self):
        self.config = config
        self.caveman_active = False
        self.caveman_level = 'full'
        self.stats = CavemanStats()
        self.chain = AgentChain(config)

    def process(self, user_message: str) -> str:
        """Main entry point"""

        # 1. Check for skill activation
        skill_name, skill_config = route_skill(user_message)

        if skill_name == 'caveman':
            # Activate caveman mode
            self.caveman_active = True
            self.caveman_level = skill_config['level']
            return f"Caveman mode {self.caveman_level} ON. Brain still big."

        if skill_name == 'caveman-stats':
            return self.stats.get_report(skill_config.get('share', False))

        # 2. Check for agent routing
        agent_name, agent_config = route_agent(user_message)

        if agent_name == 'cavecrew-investigator':
            response = self.chain.start_investigation(user_message)
        elif agent_name == 'cavecrew-builder':
            response = self.chain.build_from_investigation(user_message)
        elif agent_name == 'cavecrew-reviewer':
            response = self.chain.review_builder_output()
        else:
            # Default: main agent
            response = run_main_agent(user_message)

        # 3. Apply caveman formatting if active
        if self.caveman_active:
            response = apply_caveman(response, self.caveman_level)
            self.stats.record_call(self.caveman_level, len(response), len(response))

        # 4. Handle deactivation
        if any(word in user_message.lower() for word in ['stop caveman', 'normal mode']):
            self.caveman_active = False
            response += "\n\nCaveman mode OFF. Normal mode ON."

        return response

# Usage
agent_system = CavemanAgentSystem()
response = agent_system.process("Find where user validation happens")
print(response)
```

## Deployment Checklist

- [ ] Load AGENT_INSTRUCTIONS.md into system prompt
- [ ] Parse agent-config.json for agent definitions
- [ ] Implement skill router (caveman modes, etc.)
- [ ] Implement agent router (investigator, builder, reviewer)
- [ ] Implement caveman formatter (drop rules, abbreviations, etc.)
- [ ] Implement auto-clarity exceptions
- [ ] Implement Find → Build → Review chain
- [ ] Track token usage with CavemanStats
- [ ] Add /caveman, /caveman-commit, etc. handlers
- [ ] Test with CHEATSHEET.md examples
- [ ] Add to team docs
- [ ] Get feedback from users

---

**Questions?** See AGENT_USAGE_GUIDE.md or check https://github.com/JuliusBrussee/caveman
