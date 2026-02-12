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
📊 Tokens: ~3,200 | Cost: ~$0.18 | Turns: 5
   View full report? → /tokenusage show
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

| Command | Description |
|---------|-------------|
| `/tokenusage show` | Display ASCII visualization of token usage |
| `/tokenusage export` | Export session data to JSON and HTML |
| `/tokenusage analyze` | Get prompt improvement suggestions |
| `/tokenusage reset` | Reset tracking for a new session |

## Token Estimation

Since direct API token counts aren't always available, use heuristic estimation:

### Character-to-Token Ratios

| Content Type | Divisor | Example |
|--------------|---------|---------|
| English text | 4.0 | 400 chars ≈ 100 tokens |
| Code | 3.5 | 350 chars ≈ 100 tokens |
| JSON/YAML | 3.8 | 380 chars ≈ 100 tokens |
| URLs/paths | 3.0 | 300 chars ≈ 100 tokens |

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

| Content | Approximate Tokens |
|---------|-------------------|
| 1 paragraph (~500 chars) | 125 tokens |
| 1 function (~20 lines) | 150 tokens |
| 1 page of text | 400 tokens |
| Code file (~100 lines) | 700 tokens |

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
  "estimated_cost": 0.00
}
```

## Cost Calculation

### Model Pricing (per 1M tokens, as of 2025)

| Provider | Model | Input | Output |
|----------|-------|-------|--------|
| Anthropic | Claude Opus 4 | $15.00 | $75.00 |
| Anthropic | Claude Sonnet 4 | $3.00 | $15.00 |
| Anthropic | Claude Haiku | $0.25 | $1.25 |
| OpenAI | GPT-4o | $2.50 | $10.00 |
| OpenAI | GPT-4o-mini | $0.15 | $0.60 |
| OpenAI | o1 | $15.00 | $60.00 |
| Google | Gemini 1.5 Pro | $1.25 | $5.00 |
| Google | Gemini 2.0 Flash | $0.10 | $0.40 |

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

## References

- `references/prompt-best-practices.md` - Detailed prompt optimization guide
- `references/html-template.html` - HTML export template

## Installation

See `README.md` for installation instructions for:
- Claude Code
- Cursor
- Continue.dev
- Standalone usage
