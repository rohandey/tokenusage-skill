# Token Usage Skill

Track token usage, visualize consumption patterns, and get prompt improvement suggestions for LLM-powered coding assistants.

## Features

- **Token Tracking**: Estimate input/output tokens per conversation turn
- **Cost Estimation**: Calculate costs based on current model pricing
- **Visualization**: ASCII bar charts and HTML reports
- **Prompt Analysis**: Get suggestions to reduce token usage
- **Automatic Summaries**: Proactive mini-reports without manual invocation

## Installation

### Claude Code

```bash
git clone https://github.com/rohandey/tokenusage-skill.git ~/.claude/skills/tokenusage-skill
```

### Cursor

```bash
git clone https://github.com/rohandey/tokenusage-skill.git ~/.cursor/skills/tokenusage-skill
```

### Codex

```bash
git clone https://github.com/rohandey/tokenusage-skill.git ~/.codex/skills/tokenusage-skill
```

## Auto-Enable

Add this to your global config file to enable automatic tracking in every session:

| Tool        | Config File                  |
| ----------- | ---------------------------- |
| Claude Code | `~/.claude/CLAUDE.md`        |
| Cursor      | `~/.cursor/rules/global.mdc` |
| Codex       | `~/.codex/instructions.md`   |

```
## Automatic Token Usage Tracking (ALWAYS DO THIS)

MUST show mini token summary at the END of every 5th response. Count turns starting from 1.

Refer to tokenusage-skill/SKILL.md for format, estimation rules, and commands.
```

## Uninstall

```bash
# Claude Code
rm -rf ~/.claude/skills/tokenusage-skill

# Cursor
rm -rf ~/.cursor/skills/tokenusage-skill

# Codex
rm -rf ~/.codex/skills/tokenusage-skill
```

---

## Automatic Behavior

Once active, the LLM shows mini token summaries when:

- Every 5 conversation turns
- After large code generation (>100 lines)
- After multiple tool calls (3+)
- When session cost exceeds $0.25

**Format:**

```
───────────────────────────────────────
📊 Tokens: ~3,200 | Context: 22% | Turns: 5
───────────────────────────────────────
```

---

## Standalone

Use the Python script for any tool or post-session analysis:

```bash
# Install (optional, for accurate OpenAI counts)
pip install tiktoken

# Estimate tokens for text
python adapters/tokenusage.py --input "your prompt here"

# Analyze a conversation file
python adapters/tokenusage.py --file conversation.json

# Interactive mode
python adapters/tokenusage.py --interactive

# Specify model for cost calculation
python adapters/tokenusage.py --input "text" --model gpt-4o
```

---

## Commands Reference

| Command                    | Description                             |
| -------------------------- | --------------------------------------- |
| `/tokenusage`              | Display mini token summary              |
| `/tokenusage show`         | Display full ASCII dashboard            |
| `/tokenusage advice`       | Get specific prompt rewrite suggestions |
| `/tokenusage analyze`      | Get token efficiency analysis           |
| `/tokenusage model-suggest`| Recommend cheaper model for task        |
| `/tokenusage context`      | Show context window usage               |
| `/tokenusage compare`      | Compare session to typical usage        |
| `/tokenusage cache-hints`  | Identify cacheable repeated context     |
| `/tokenusage export`       | Export session data to JSON/HTML        |
| `/tokenusage reset`        | Reset tracking for new session          |
| `/tokenusage quiet`        | Disable automatic summaries             |
| `/tokenusage auto`         | Re-enable automatic summaries           |

---

## Token Estimation

Since direct API token counts aren't always available, the skill uses character-based heuristics:

| Content Type | Chars per Token | Example                |
| ------------ | --------------- | ---------------------- |
| English text | 4.0             | 400 chars ≈ 100 tokens |
| Code         | 3.5             | 350 chars ≈ 100 tokens |
| JSON/YAML    | 3.8             | 380 chars ≈ 100 tokens |
| URLs/paths   | 3.0             | 300 chars ≈ 100 tokens |

### Quick Estimates

| Content                  | Approximate Tokens |
| ------------------------ | ------------------ |
| 1 paragraph (~500 chars) | ~125 tokens        |
| 1 function (~20 lines)   | ~150 tokens        |
| 1 page of text           | ~400 tokens        |
| Code file (~100 lines)   | ~700 tokens        |

---

## Cost Reference (2025)

| Model            | Input (per 1M) | Output (per 1M) |
| ---------------- | -------------- | --------------- |
| Claude Opus 4    | $15.00         | $75.00          |
| Claude Sonnet 4  | $3.00          | $15.00          |
| Claude Haiku     | $0.25          | $1.25           |
| GPT-4o           | $2.50          | $10.00          |
| GPT-4o-mini      | $0.15          | $0.60           |
| GPT-o1           | $15.00         | $60.00          |
| Gemini 1.5 Pro   | $1.25          | $5.00           |
| Gemini 2.0 Flash | $0.10          | $0.40           |

---

## Example Output

### Full Dashboard (`/tokenusage show`)

```
╔══════════════════════════════════════════════════════════════════╗
║                     TOKEN USAGE DASHBOARD                        ║
╠══════════════════════════════════════════════════════════════════╣
║ Model: claude-sonnet-4               Session: abc123             ║
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
║  Total Tokens: 3,901 | Est. Cost: $0.06                          ║
╚══════════════════════════════════════════════════════════════════╝
```

---

## Project Structure

```
tokenusage-skill/
├── README.md                        # This file
├── SKILL.md                         # Skill instructions (works in any LLM)
├── LICENSE                          # MIT License
├── references/
│   ├── prompt-best-practices.md     # Prompt optimization guide
│   └── html-template.html           # HTML export template
└── adapters/
    └── tokenusage.py                # Standalone Python script
```

---

## Limitations

- **Estimates only**: No access to real API token counts
- **Heuristic-based**: Character ratios are approximations
- **Session-scoped**: Cannot persist data across sessions automatically
- **LLM-dependent**: Automatic summaries rely on the LLM following instructions

For accurate token counts:

- **OpenAI models**: Use the Python script with `tiktoken`
- **Claude models**: Check [Anthropic Console](https://console.anthropic.com) after session

---

## Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Add tests if applicable
4. Submit a pull request

---

## License

MIT License - see [LICENSE](LICENSE) for details.

---

## Related Resources

- [Anthropic Token Counting](https://docs.anthropic.com/en/docs/build-with-claude/token-counting)
- [OpenAI Tokenizer](https://platform.openai.com/tokenizer)
- [tiktoken Library](https://github.com/openai/tiktoken)
