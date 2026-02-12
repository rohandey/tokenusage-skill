# Cursor Rules for Token Usage Tracking

Add this content to your `.cursorrules` file in your project root.

---

## Token Usage Tracking Rules

When the user mentions "token usage", "track tokens", or "show tokens", follow these guidelines:

### Token Estimation

Estimate tokens using character counts:
- English text: characters ÷ 4
- Code: characters ÷ 3.5
- JSON/YAML: characters ÷ 3.8
- URLs/paths: characters ÷ 3

### Per-Turn Tracking

For each conversation turn, mentally track:
1. Input tokens (user message)
2. Output tokens (your response)
3. Running cumulative total

### When Asked to Show Token Usage

Display in this format:

```
Token Usage Summary
───────────────────────────────────────
Turn 1: ████████░░░░  800 tokens
Turn 2: ██████░░░░░░  600 tokens
Turn 3: ████████████  1,200 tokens
───────────────────────────────────────
Total: 2,600 tokens
Est. Cost: $0.05 (GPT-4o rates)
```

### Cost Rates (per 1M tokens)

- GPT-4o: Input $2.50, Output $10.00
- GPT-4o-mini: Input $0.15, Output $0.60
- Claude Sonnet 4: Input $3.00, Output $15.00

### Prompt Analysis

When asked to analyze prompts for efficiency:

1. **Check for redundancy** - Repeated context in follow-ups
2. **Check for verbosity** - Unnecessary politeness or filler
3. **Check for constraints** - Missing output format/length specs
4. **Suggest improvements** - Specific, actionable recommendations

### Example Analysis Output

```
Prompt Analysis
───────────────────────────────────────
[HIGH] Redundancy detected
  - Context repeated from Turn 1
  - Potential savings: ~200 tokens

[MEDIUM] Missing constraints
  - No output format specified
  - Add: "respond in 3 bullet points"

[LOW] Minor verbosity
  - "I was wondering if you could" → "Please"
───────────────────────────────────────
```

---

## Full .cursorrules Content

Copy everything below this line into your `.cursorrules` file:

```
# Token Usage Tracking

## Estimation Ratios
- Text: chars ÷ 4
- Code: chars ÷ 3.5
- JSON: chars ÷ 3.8

## Commands
- "show token usage" → Display ASCII bar chart of session tokens
- "analyze my prompts" → Review prompts for efficiency improvements
- "token cost" → Calculate estimated cost based on model rates

## Always
- Track approximate token counts mentally throughout conversation
- When showing usage, include both per-turn and cumulative totals
- Provide cost estimates using GPT-4o rates unless user specifies otherwise

## Cost Reference (per 1M tokens)
- GPT-4o: $2.50 input, $10.00 output
- GPT-4o-mini: $0.15 input, $0.60 output
- Claude Sonnet: $3.00 input, $15.00 output
```
