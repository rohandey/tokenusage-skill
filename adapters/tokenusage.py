#!/usr/bin/env python3
"""
Token Usage Estimator - Standalone Script

Estimate token counts and costs for LLM prompts and conversations.

Usage:
    python tokenusage.py --input "your prompt here"
    python tokenusage.py --file conversation.json
    python tokenusage.py --interactive

Requirements:
    - Python 3.7+
    - tiktoken (optional, for accurate OpenAI token counts)
"""

import argparse
import json
import math
import re
import sys
from datetime import datetime
from typing import Optional

# Try to import tiktoken for accurate OpenAI tokenization
try:
    import tiktoken
    TIKTOKEN_AVAILABLE = True
except ImportError:
    TIKTOKEN_AVAILABLE = False


# Model pricing per 1M tokens (as of 2025)
PRICING = {
    "claude-opus-4": {"input": 15.00, "output": 75.00},
    "claude-sonnet-4": {"input": 3.00, "output": 15.00},
    "claude-haiku": {"input": 0.25, "output": 1.25},
    "gpt-4o": {"input": 2.50, "output": 10.00},
    "gpt-4o-mini": {"input": 0.15, "output": 0.60},
    "gpt-o1": {"input": 15.00, "output": 60.00},
    "gemini-1.5-pro": {"input": 1.25, "output": 5.00},
    "gemini-2.0-flash": {"input": 0.10, "output": 0.40},
}


def estimate_tokens_heuristic(text: str, content_type: str = "text") -> int:
    """
    Estimate token count using character-based heuristics.

    Args:
        text: The text to estimate tokens for
        content_type: Type of content ('text', 'code', 'json')

    Returns:
        Estimated token count
    """
    # Normalize whitespace
    normalized = re.sub(r'\s+', ' ', text.strip())
    char_count = len(normalized)

    # Character-to-token ratios
    ratios = {
        "text": 4.0,
        "code": 3.5,
        "json": 3.8,
        "url": 3.0,
    }

    ratio = ratios.get(content_type, 4.0)
    return math.ceil(char_count / ratio)


def estimate_tokens_tiktoken(text: str, model: str = "gpt-4o") -> int:
    """
    Estimate tokens using OpenAI's tiktoken library.

    Args:
        text: The text to tokenize
        model: The model to use for encoding

    Returns:
        Actual token count
    """
    if not TIKTOKEN_AVAILABLE:
        return estimate_tokens_heuristic(text)

    try:
        encoding = tiktoken.encoding_for_model(model)
        return len(encoding.encode(text))
    except Exception:
        return estimate_tokens_heuristic(text)


def detect_content_type(text: str) -> str:
    """Detect if text is code, JSON, or plain text."""
    # Check for JSON
    text_stripped = text.strip()
    if text_stripped.startswith('{') or text_stripped.startswith('['):
        try:
            json.loads(text_stripped)
            return "json"
        except json.JSONDecodeError:
            pass

    # Check for code patterns
    code_patterns = [
        r'def \w+\(',           # Python function
        r'function \w+\(',      # JavaScript function
        r'class \w+',           # Class definition
        r'import \w+',          # Import statement
        r'const \w+ =',         # JavaScript const
        r'let \w+ =',           # JavaScript let
        r'var \w+ =',           # JavaScript var
        r'if \(.+\) \{',        # If statement with braces
        r'for \(.+\) \{',       # For loop
        r'=>',                  # Arrow function
        r'async ',              # Async keyword
    ]

    for pattern in code_patterns:
        if re.search(pattern, text):
            return "code"

    return "text"


def calculate_cost(input_tokens: int, output_tokens: int, model: str) -> dict:
    """Calculate cost based on token counts and model pricing."""
    pricing = PRICING.get(model, PRICING["claude-sonnet-4"])

    input_cost = (input_tokens / 1_000_000) * pricing["input"]
    output_cost = (output_tokens / 1_000_000) * pricing["output"]

    return {
        "input": round(input_cost, 6),
        "output": round(output_cost, 6),
        "total": round(input_cost + output_cost, 6),
    }


def generate_bar(value: int, max_value: int, width: int = 20) -> str:
    """Generate an ASCII progress bar."""
    if max_value == 0:
        return '░' * width

    fill = min(width, math.ceil((value / max_value) * width))
    return '█' * fill + '░' * (width - fill)


def display_usage(turns: list, model: str = "claude-sonnet-4"):
    """Display token usage in ASCII format."""
    if not turns:
        print("No usage data to display.")
        return

    max_tokens = max(t.get("total", 0) for t in turns)
    total_input = sum(t.get("input", 0) for t in turns)
    total_output = sum(t.get("output", 0) for t in turns)
    total_tokens = total_input + total_output

    cost = calculate_cost(total_input, total_output, model)

    print("╔════════════════════════════════════════════════════════════════╗")
    print("║                    TOKEN USAGE DASHBOARD                       ║")
    print("╠════════════════════════════════════════════════════════════════╣")
    print(f"║ Model: {model:<20}                                   ║")
    print("╠════════════════════════════════════════════════════════════════╣")
    print("║                                                                ║")
    print("║  Token Usage by Turn:                                          ║")
    print("║  ─────────────────────────────────────────────────────────────║")

    for turn in turns:
        turn_num = turn.get("turn", "?")
        turn_total = turn.get("total", 0)
        turn_input = turn.get("input", 0)
        turn_output = turn.get("output", 0)
        bar = generate_bar(turn_total, max_tokens)
        print(f"║  Turn {turn_num}: {bar}  {turn_total:,} tokens (In: {turn_input:,}, Out: {turn_output:,})")

    print("║                                                                ║")
    print("║  ─────────────────────────────────────────────────────────────║")
    print("║  Distribution:                                                 ║")

    if total_tokens > 0:
        input_pct = (total_input / total_tokens) * 100
        output_pct = (total_output / total_tokens) * 100
        print(f"║  Input:  {generate_bar(total_input, total_tokens)}  {total_input:,} tokens ({input_pct:.0f}%)")
        print(f"║  Output: {generate_bar(total_output, total_tokens)}  {total_output:,} tokens ({output_pct:.0f}%)")

    print("║                                                                ║")
    print("╠════════════════════════════════════════════════════════════════╣")
    print("║  TOTALS                                                        ║")
    print("║  ─────────────────────────────────────────────────────────────║")
    print(f"║  Total Tokens: {total_tokens:,}")
    print(f"║  Estimated Cost: ${cost['total']:.4f} (Input: ${cost['input']:.4f}, Output: ${cost['output']:.4f})")
    print("╚════════════════════════════════════════════════════════════════╝")


def export_json(turns: list, model: str = "claude-sonnet-4") -> dict:
    """Export usage data as JSON."""
    total_input = sum(t.get("input", 0) for t in turns)
    total_output = sum(t.get("output", 0) for t in turns)
    total_tools = sum(t.get("tools", 0) for t in turns)

    cost = calculate_cost(total_input, total_output, model)

    return {
        "session_id": datetime.now().strftime("%Y%m%d_%H%M%S"),
        "model": model,
        "timestamp": datetime.now().isoformat(),
        "turns": turns,
        "totals": {
            "input": total_input,
            "output": total_output,
            "tools": total_tools,
            "total": total_input + total_output + total_tools,
        },
        "estimated_cost": {
            "input": cost["input"],
            "output": cost["output"],
            "total": cost["total"],
            "currency": "USD",
        }
    }


def analyze_text(text: str) -> dict:
    """Analyze a single text input."""
    content_type = detect_content_type(text)

    if TIKTOKEN_AVAILABLE:
        tokens = estimate_tokens_tiktoken(text)
        method = "tiktoken"
    else:
        tokens = estimate_tokens_heuristic(text, content_type)
        method = "heuristic"

    return {
        "text_preview": text[:100] + "..." if len(text) > 100 else text,
        "characters": len(text),
        "tokens": tokens,
        "content_type": content_type,
        "method": method,
    }


def interactive_mode():
    """Run in interactive mode for quick estimates."""
    print("Token Usage Estimator - Interactive Mode")
    print("Enter text to estimate tokens (Ctrl+C to exit)")
    print("-" * 50)

    turns = []
    turn_num = 0

    while True:
        try:
            print("\n[Input] Enter your prompt (empty line to finish):")
            lines = []
            while True:
                line = input()
                if line == "":
                    break
                lines.append(line)

            if not lines:
                continue

            input_text = "\n".join(lines)
            input_analysis = analyze_text(input_text)

            print(f"\nInput: {input_analysis['tokens']} tokens ({input_analysis['content_type']})")

            print("\n[Output] Enter the response (empty line to finish):")
            lines = []
            while True:
                line = input()
                if line == "":
                    break
                lines.append(line)

            output_text = "\n".join(lines) if lines else ""
            output_analysis = analyze_text(output_text) if output_text else {"tokens": 0}

            print(f"Output: {output_analysis['tokens']} tokens")

            turn_num += 1
            turns.append({
                "turn": turn_num,
                "input": input_analysis["tokens"],
                "output": output_analysis["tokens"],
                "total": input_analysis["tokens"] + output_analysis["tokens"],
            })

            print(f"\nTurn {turn_num} total: {turns[-1]['total']} tokens")
            print("\nCommands: 'show' for summary, 'export' for JSON, 'quit' to exit")

            cmd = input("Command (or press Enter to continue): ").strip().lower()

            if cmd == "show":
                display_usage(turns)
            elif cmd == "export":
                print(json.dumps(export_json(turns), indent=2))
            elif cmd in ("quit", "exit", "q"):
                break

        except KeyboardInterrupt:
            print("\n\nFinal Summary:")
            display_usage(turns)
            break
        except EOFError:
            break


def main():
    parser = argparse.ArgumentParser(
        description="Estimate token counts and costs for LLM prompts"
    )
    parser.add_argument(
        "--input", "-i",
        type=str,
        help="Text to estimate tokens for"
    )
    parser.add_argument(
        "--file", "-f",
        type=str,
        help="JSON file containing conversation data"
    )
    parser.add_argument(
        "--model", "-m",
        type=str,
        default="claude-sonnet-4",
        choices=list(PRICING.keys()),
        help="Model for cost calculation"
    )
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="Run in interactive mode"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output as JSON"
    )

    args = parser.parse_args()

    if args.interactive:
        interactive_mode()
        return

    if args.input:
        analysis = analyze_text(args.input)
        cost = calculate_cost(analysis["tokens"], 0, args.model)

        if args.json:
            print(json.dumps({
                **analysis,
                "model": args.model,
                "estimated_cost": cost,
            }, indent=2))
        else:
            print(f"Characters: {analysis['characters']}")
            print(f"Tokens: {analysis['tokens']} ({analysis['method']})")
            print(f"Content type: {analysis['content_type']}")
            print(f"Est. cost (input): ${cost['input']:.6f}")
        return

    if args.file:
        with open(args.file, 'r') as f:
            data = json.load(f)

        if isinstance(data, list):
            turns = data
        elif "turns" in data:
            turns = data["turns"]
        else:
            print("Error: Invalid file format. Expected list of turns or {turns: [...]}")
            sys.exit(1)

        if args.json:
            print(json.dumps(export_json(turns, args.model), indent=2))
        else:
            display_usage(turns, args.model)
        return

    # No arguments - show help
    parser.print_help()


if __name__ == "__main__":
    main()
