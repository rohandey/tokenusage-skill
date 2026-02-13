---
name: tokenusage
description: Track token usage in LLM sessions, visualize consumption patterns, and get prompt improvement suggestions. Works with Claude Code, Cursor, Continue.dev, and other AI coding assistants.
trigger: auto
---

# Token Usage Skill

Track token usage, visualize consumption patterns, and get prompt improvement suggestions for any LLM-powered coding assistant.

## Automatic Behavior (Proactive Mode)

When this skill is active, **automatically show a mini token summary** under these conditions:

### When to Show Mini Summary

- After every **5 conversation turns**
- After a **large code generation** (>100 lines or >2000 tokens estimated)
- After **multiple tool calls** in a single response (3+ tools)
- When **estimated session cost exceeds $0.25**

### Mini Summary Format

Display this compact format at the end of your response:

```
───────────────────────────────────────
📊 Tokens: ~3,200 | Context: 22% | Turns: 5
   View full report? → /tokenusage show
   Get advice → /tokenusage advice
───────────────────────────────────────
```

### When NOT to Show

- User is in the middle of debugging (rapid back-and-forth)
- Previous response already showed a summary
- User explicitly disabled with `/tokenusage quiet`

### Quiet Mode

If user says `/tokenusage quiet`, stop showing automatic summaries until:

- User says `/tokenusage auto` to re-enable
- A new session starts

## Commands

| Command                   | Description                                |
| ------------------------- | ------------------------------------------ |
| `/tokenusage`             | Show help menu with all commands           |
| `/tokenusage summary`     | Display mini token summary                 |
| `/tokenusage show`        | Display full ASCII visualization dashboard |
| `/tokenusage advice`      | Get specific prompt rewrite suggestions    |
| `/tokenusage analyze`     | Get token efficiency analysis              |
| `/tokenusage model-suggest` | Recommend cheaper model for task         |
| `/tokenusage context`     | Show context window usage                  |
| `/tokenusage compare`     | Compare session to typical usage           |
| `/tokenusage cache-hints` | Identify cacheable repeated context        |
| `/tokenusage export`      | Export session data to JSON and HTML       |
| `/tokenusage reset`       | Reset tracking for a new session           |
| `/tokenusage quiet`       | Disable automatic summaries                |
| `/tokenusage auto`        | Re-enable automatic summaries              |

## Default Behavior: Help Menu

When user types `/tokenusage` without any arguments, display this help menu:

```
╔══════════════════════════════════════════════════════════════════╗
║                    TOKEN USAGE SKILL - HELP                      ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                  ║
║  Available Commands:                                             ║
║  ───────────────────────────────────────────────────────────────║
║                                                                  ║
║  /tokenusage summary       📈 Quick session summary             ║
║  /tokenusage show          📊 Full token dashboard              ║
║  /tokenusage advice        💡 Prompt rewrite suggestions        ║
║  /tokenusage analyze       🔍 Token efficiency analysis         ║
║  /tokenusage model-suggest 🤖 Cheaper model recommendation      ║
║  /tokenusage context       📦 Context window usage              ║
║  /tokenusage compare       ⚖️  Compare to typical usage          ║
║  /tokenusage cache-hints   ♻️  Cacheable content hints           ║
║  /tokenusage export        💾 Export to JSON/HTML               ║
║  /tokenusage reset         🔄 Reset session tracking            ║
║  ───────────────────────────────────────────────────────────────║
║  /tokenusage quiet         🔇 Disable auto summaries            ║
║  /tokenusage auto          🔊 Enable auto summaries             ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
```

### Summary Format (`/tokenusage summary`)

```
───────────────────────────────────────
📊 Tokens: ~X,XXX | Context: XX% | Turn: X
   View full report? → /tokenusage show
   Get advice → /tokenusage advice
───────────────────────────────────────
```

**Calculating Context % for summary:**

- Estimate system prompts: ~18,000 tokens (base)
- Add ~2,000-4,000 tokens per turn (conversation + tools)
- Context % = total / 200,000 (for Claude models)

### Model Suggest (`/tokenusage model-suggest`)

Analyze the session and recommend if a cheaper model would suffice.

```
╔══════════════════════════════════════════════════════════════════╗
║                     MODEL RECOMMENDATION                         ║
╠══════════════════════════════════════════════════════════════════╣
║  Current: Claude Opus 4.5                                        ║
║  Session cost: $0.93                                             ║
║                                                                  ║
║  💡 SUGGESTION: Switch to Sonnet 4                               ║
║  ───────────────────────────────────────────────────────────────║
║  This session involves mostly:                                   ║
║  • File edits (80%)                                              ║
║  • Simple Q&A (15%)                                              ║
║  • Light reasoning (5%)                                          ║
║                                                                  ║
║  Estimated cost with Sonnet: $0.12 (87% savings)                 ║
║                                                                  ║
║  ⚠️ Keep Opus for: Complex architecture, nuanced decisions       ║
╚══════════════════════════════════════════════════════════════════╝
```

### Context (`/tokenusage context`)

Show context window usage and warn when approaching limits.

**How to Calculate Context %:**

```
context_tokens = system_prompts + conversation_history + tool_results + loaded_files
context_percent = (context_tokens / max_context_window) × 100
```

**What counts toward context:**

- System prompts & tool definitions (~15,000-20,000 tokens)
- All user messages in conversation
- All assistant responses in conversation
- Tool call results (file reads, search results, etc.)
- Loaded skill files (SKILL.md, etc.)

**Model context windows:**
| Model | Max Context |
|-------|-------------|
| Claude Opus 4.5 | 200,000 |
| Claude Sonnet 4 | 200,000 |
| GPT-4o | 128,000 |
| Gemini 1.5 Pro | 1,000,000 |

```
╔══════════════════════════════════════════════════════════════════╗
║                     CONTEXT WINDOW STATUS                        ║
╠══════════════════════════════════════════════════════════════════╣
║  Model: Claude Opus 4.5                                          ║
║  Max context: 200,000 tokens                                     ║
║                                                                  ║
║  Usage: ████████░░░░░░░░░░░░  80,000 / 200,000 (40%)            ║
║                                                                  ║
║  Breakdown:                                                      ║
║  • System prompts:  ~18,000 tokens                               ║
║  • Conversation:    ~42,000 tokens                               ║
║  • Tool results:    ~20,000 tokens                               ║
║                                                                  ║
║  ✅ Healthy - room for ~60 more turns                            ║
║                                                                  ║
║  ⚠️ At 80%: Consider /compact or start new session               ║
╚══════════════════════════════════════════════════════════════════╝
```

### Compare (`/tokenusage compare`)

Compare current session to typical patterns.

```
╔══════════════════════════════════════════════════════════════════╗
║                     SESSION COMPARISON                           ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                  ║
║  This Session          vs    Typical Session                     ║
║  ─────────────────────────────────────────────────────────────  ║
║  Turns:    18                     15                             ║
║  Tokens:   ~22,000                ~12,000                        ║
║  Cost:     $0.93                  $0.45                          ║
║  Tools:    42 calls               25 calls                       ║
║                                                                  ║
║  📊 Analysis:                                                    ║
║  ───────────────────────────────────────────────────────────────║
║  • 47% more tool usage than typical                              ║
║  • Heavy file reading/editing session                            ║
║  • Multiple iterative refinements detected                       ║
║                                                                  ║
║  💡 Tip: Batch related changes to reduce back-and-forth          ║
╚══════════════════════════════════════════════════════════════════╝
```

### Cache Hints (`/tokenusage cache-hints`)

Identify repeated content that could benefit from prompt caching.

```
╔══════════════════════════════════════════════════════════════════╗
║                     CACHE OPTIMIZATION HINTS                     ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                  ║
║  ♻️ CACHEABLE CONTENT DETECTED                                   ║
║  ───────────────────────────────────────────────────────────────║
║                                                                  ║
║  1. System prompt (~2,500 tokens)                                ║
║     Repeated: 18 times                                           ║
║     Potential savings: ~$0.35 with prompt caching                ║
║                                                                  ║
║  2. SKILL.md content (~3,200 tokens)                             ║
║     Loaded: 6 times this session                                 ║
║     Potential savings: ~$0.15 with prompt caching                ║
║                                                                  ║
║  ───────────────────────────────────────────────────────────────║
║  TOTAL POTENTIAL SAVINGS: ~$0.50 (54% of session cost)           ║
║                                                                  ║
║  📖 Learn more: anthropic.com/news/prompt-caching                ║
╚══════════════════════════════════════════════════════════════════╝
```

## Token Estimation

Since direct API token counts aren't always available, use heuristic estimation:

### Character-to-Token Ratios

| Content Type | Divisor | Example                |
| ------------ | ------- | ---------------------- |
| English text | 4.0     | 400 chars ≈ 100 tokens |
| Code         | 3.5     | 350 chars ≈ 100 tokens |
| JSON/YAML    | 3.8     | 380 chars ≈ 100 tokens |
| URLs/paths   | 3.0     | 300 chars ≈ 100 tokens |

### Estimation Function (Pseudocode)

```
function estimateTokens(text, type = 'text'):
    normalized = normalizeWhitespace(text)
    charCount = length(normalized)

    ratios = {
        'text': 4.0,
        'code': 3.5,
        'json': 3.8,
        'url': 3.0
    }

    return ceil(charCount / ratios[type])
```

### Quick Estimates

| Content                  | Approximate Tokens |
| ------------------------ | ------------------ |
| 1 paragraph (~500 chars) | 125 tokens         |
| 1 function (~20 lines)   | 150 tokens         |
| 1 page of text           | 400 tokens         |
| Code file (~100 lines)   | 700 tokens         |

## Session Tracking

Track these metrics per conversation turn:

### Data Structure

```json
{
  "session_id": "unique-id",
  "model": "model-name",
  "started_at": "ISO-8601 timestamp",
  "turns": [
    {
      "turn": 1,
      "input_tokens": 150,
      "output_tokens": 400,
      "tool_tokens": 200,
      "total": 750,
      "cumulative": 750
    }
  ],
  "totals": {
    "input": 0,
    "output": 0,
    "tools": 0,
    "total": 0
  },
  "estimated_cost": 0.0
}
```

## Cost Calculation

### Model Pricing (per 1M tokens, as of 2025)

| Provider  | Model            | Input  | Output |
| --------- | ---------------- | ------ | ------ |
| Anthropic | Claude Opus 4    | $15.00 | $75.00 |
| Anthropic | Claude Sonnet 4  | $3.00  | $15.00 |
| Anthropic | Claude Haiku     | $0.25  | $1.25  |
| OpenAI    | GPT-4o           | $2.50  | $10.00 |
| OpenAI    | GPT-4o-mini      | $0.15  | $0.60  |
| OpenAI    | o1               | $15.00 | $60.00 |
| Google    | Gemini 1.5 Pro   | $1.25  | $5.00  |
| Google    | Gemini 2.0 Flash | $0.10  | $0.40  |

### Cost Formula

```
input_cost = (input_tokens / 1,000,000) × input_rate
output_cost = (output_tokens / 1,000,000) × output_rate
total_cost = input_cost + output_cost
```

## Visualization: Show Command

Generate ASCII bar chart:

```
╔══════════════════════════════════════════════════════════════════╗
║                     TOKEN USAGE DASHBOARD                        ║
╠══════════════════════════════════════════════════════════════════╣
║ Model: claude-sonnet-4           Session: abc123                 ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                  ║
║  Token Usage by Turn:                                            ║
║  ───────────────────────────────────────────────────────────────║
║  Turn 1: ████████████░░░░░░░░  1,234 tokens (In: 234, Out: 1000) ║
║  Turn 2: ██████░░░░░░░░░░░░░░    567 tokens (In: 167, Out: 400)  ║
║  Turn 3: ████████████████████  2,100 tokens (In: 500, Out: 1600) ║
║                                                                  ║
║  ───────────────────────────────────────────────────────────────║
║  Distribution:                                                   ║
║  Input:  ████░░░░░░░░░░░░░░░░  901 tokens (23%)                 ║
║  Output: ████████████████░░░░  3,000 tokens (77%)               ║
║                                                                  ║
╠══════════════════════════════════════════════════════════════════╣
║  TOTALS                                                          ║
║  ───────────────────────────────────────────────────────────────║
║  Total Tokens: 3,901                                             ║
║  Estimated Cost: $0.06 (Input: $0.003, Output: $0.05)           ║
╠══════════════════════════════════════════════════════════════════╣
║  ⚠️ These are estimates based on character-to-token heuristics.  ║
║  Actual usage may vary ±15%. Check your provider dashboard for   ║
║  exact counts.                                                   ║
╚══════════════════════════════════════════════════════════════════╝
```

### Bar Generation Logic

```
max_width = 20
bar_fill = round((turn_tokens / max_tokens) * max_width)
bar = '█' × bar_fill + '░' × (max_width - bar_fill)
```

## Export: Export Command

### JSON Output

```json
{
  "session_id": "abc123",
  "model": "claude-sonnet-4",
  "timestamp": "2025-02-12T10:30:00Z",
  "turns": [
    {
      "turn": 1,
      "input_tokens": 234,
      "output_tokens": 1000,
      "tool_tokens": 150,
      "total": 1384,
      "cumulative": 1384
    }
  ],
  "totals": {
    "input": 901,
    "output": 3000,
    "tools": 500,
    "total": 4401
  },
  "estimated_cost": {
    "input": 0.003,
    "output": 0.045,
    "total": 0.048,
    "currency": "USD"
  },
  "suggestions": [
    "Consider using more concise prompts",
    "Tool usage accounted for 11% of tokens"
  ]
}
```

### HTML Report Template

See `references/html-template.html` for a complete HTML report template.

## Analyze: Prompt Improvement

### Analysis Categories

**Token Efficiency**

- Redundancy: Repeated context or instructions
- Verbosity: Overly wordy requests
- Context bloat: Unnecessarily large context windows

**Clarity**

- Ambiguous requests: Suggest specific phrasing
- Missing constraints: Recommend bounds/limits
- Structure: Propose numbered steps or bullets

**Best Practices**

- Few-shot: Suggest examples for complex tasks
- System prompts: Move repeated instructions
- Chunking: Break large tasks into smaller ones

### Output Format

```
╔══════════════════════════════════════════════════════════════════╗
║                  PROMPT IMPROVEMENT SUGGESTIONS                  ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                  ║
║  [HIGH] Reduce Redundancy                                        ║
║  ───────────────────────────────────────────────────────────────║
║  Found 3 instances of repeated context. Consider referencing     ║
║  earlier context instead of restating.                           ║
║  Potential savings: ~450 tokens                                  ║
║                                                                  ║
║  [MEDIUM] Add Specificity                                        ║
║  ───────────────────────────────────────────────────────────────║
║  Turn 2 request was broad. Adding constraints could reduce       ║
║  output tokens by focusing the response.                         ║
║                                                                  ║
║  [LOW] Use Structured Output                                     ║
║  ───────────────────────────────────────────────────────────────║
║  Consider requesting JSON/list format for data-heavy responses   ║
║  to improve parsability and reduce prose overhead.               ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
```

## Advice: Prompt Rewrite Suggestions

The `/tokenusage advice` command reviews the user's actual prompts from the session and suggests specific rewrites.

### Output Format

```
╔══════════════════════════════════════════════════════════════════╗
║                     PROMPT ADVICE                                ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                  ║
║  Turn 3:                                                         ║
║  ───────────────────────────────────────────────────────────────║
║  ❌ Original: "Can you please help me update the README file     ║
║     to show the proper clone command for other platforms?"       ║
║                                                                  ║
║  ✅ Better: "Add clone commands for Cursor/Codex to README"      ║
║                                                                  ║
║  💡 Why: Removed filler words, made request direct               ║
║     Savings: ~15 tokens                                          ║
║                                                                  ║
║  Turn 7:                                                         ║
║  ───────────────────────────────────────────────────────────────║
║  ❌ Original: "I think you are confused ... only skill.md        ║
║     dont have the full content for the skill"                    ║
║                                                                  ║
║  ✅ Better: "SKILL.md alone isn't enough - needs adapter files"  ║
║                                                                  ║
║  💡 Why: State the issue directly, skip meta-commentary          ║
║     Savings: ~10 tokens                                          ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
```

### Advice Categories

- **Filler removal**: "Can you please..." → Direct request
- **Specificity**: Vague ask → Concrete action
- **Context reduction**: Repeating info → Reference earlier turns
- **Format requests**: Add output constraints to reduce response length

## References

- `references/prompt-best-practices.md` - Detailed prompt optimization guide
- `references/html-template.html` - HTML export template

## Installation

See `README.md` for installation instructions for:

- Claude Code
- Cursor
- Continue.dev
- Standalone usage
