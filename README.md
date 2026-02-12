# Token Usage Skill

Track token usage, visualize consumption patterns, and get prompt improvement suggestions for LLM-powered coding assistants.

## Features

- **Token Tracking**: Estimate input/output tokens per conversation turn
- **Cost Estimation**: Calculate costs based on current model pricing
- **Visualization**: ASCII bar charts and HTML reports
- **Prompt Analysis**: Get suggestions to reduce token usage
- **Automatic Summaries**: Proactive mini-reports without manual invocation

## Quick Start (Any LLM)

Add this to your assistant's rules/instructions:

```
## Token Tracking
Show mini token summary (tokens/cost/turns) every 5 turns, after large code generation, or 3+ tool calls.
Estimate: text ÷ 4, code ÷ 3.5, JSON ÷ 3.8 chars per token.
```

**Where to add it:**

| Tool | Location |
|------|----------|
| Claude Code | `~/.claude/CLAUDE.md` |
| Cursor | `.cursorrules` |
| GitHub Copilot | `.github/copilot-instructions.md` |
| Windsurf | Cascade rules |
| Sourcegraph Cody | Custom instructions in settings |
| Continue.dev | `~/.continue/config.json` ([see format](#continuedev)) |
| Aider | `.aider.conf.yml` or `--system-prompt` |
| Any other LLM | System prompt or custom instructions |

That's it! The LLM will now show token summaries automatically.

---

## Claude Code (Advanced)

For full dashboard and export features, also install the skill:

```bash
git clone https://github.com/rohandey/tokenusage-skill.git ~/.claude/skills/tokenusage-skill
```

Then use these commands:

```
/tokenusage show      # Full ASCII dashboard
/tokenusage export    # Export to JSON/HTML
/tokenusage analyze   # Get optimization tips
/tokenusage quiet     # Disable auto summaries
/tokenusage auto      # Re-enable auto summaries
```

---

## Continue.dev

Add to `~/.continue/config.json`:

```json
{
  "customCommands": [
    {
      "name": "tokenusage",
      "description": "Show token summary",
      "prompt": "Show mini token summary (tokens/cost/turns). Estimate: text ÷ 4, code ÷ 3.5, JSON ÷ 3.8."
    }
  ]
}
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
📊 Tokens: ~3,200 | Cost: ~$0.18 | Turns: 5
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

| Command               | Description                        |
| --------------------- | ---------------------------------- |
| `/tokenusage show`    | Display full ASCII dashboard       |
| `/tokenusage export`  | Export session data to JSON/HTML   |
| `/tokenusage analyze` | Get prompt improvement suggestions |
| `/tokenusage reset`   | Reset tracking for a new session   |
| `/tokenusage quiet`   | Disable automatic summaries        |
| `/tokenusage auto`    | Re-enable automatic summaries      |

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
├── SKILL.md                         # Main skill definition
├── LICENSE                          # MIT License
├── references/
│   ├── prompt-best-practices.md     # Prompt optimization guide
│   └── html-template.html           # HTML export template
└── adapters/
    ├── cursorrules.md               # Cursor adapter rules
    ├── continue-config.json         # Continue.dev config
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
