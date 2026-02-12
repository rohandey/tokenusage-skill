# Prompt Best Practices for Token Efficiency

A comprehensive guide to writing prompts that minimize token usage while maximizing response quality.

## Token-Efficient Prompt Patterns

### 1. Be Direct and Specific

**Inefficient (42 tokens):**
```
I was wondering if you could possibly help me with something. I need to write
a function that does sorting. Could you write a Python function that sorts a list?
```

**Efficient (12 tokens):**
```
Write a Python function to sort a list using quicksort.
```

**Savings: 71%**

### 2. Use Structured Requests

**Inefficient:**
```
Can you give me information about error handling? I want to know what types
there are, how to use them, and some examples would be nice too.
```

**Efficient:**
```
Error handling in Python:
1. List exception types
2. Show try/except syntax
3. One example each
```

**Benefits:**
- Clearer expectations
- More focused responses
- Easier to parse output

### 3. Reference Previous Context

**Inefficient:**
```
Remember the function we wrote earlier that processes user data and validates
the email field and checks the age is over 18? Can you add password validation
to that same function?
```

**Efficient:**
```
Add password validation to the previous processUser function.
```

**Rule:** If context is already in the conversation, reference it—don't repeat it.

### 4. Constrain Output Length

**Inefficient:**
```
Explain how databases work.
```

**Efficient:**
```
Explain database indexing in 3 sentences.
```

**Token impact:** Open-ended prompts often generate 500+ tokens. Constrained prompts target 50-100.

### 5. Request Specific Formats

**Inefficient:**
```
What are the pros and cons of React vs Vue?
```

**Efficient:**
```
React vs Vue comparison as a markdown table: columns for Performance,
Learning Curve, Ecosystem, Bundle Size.
```

**Benefits:**
- Tables are more token-dense than prose
- Easier to compare
- No filler words

## Common Wasteful Patterns to Avoid

### 1. Excessive Politeness

**Wasteful:**
```
Hello! I hope you're doing well today. I was wondering if you might be able
to help me with a small question I have. If it's not too much trouble,
could you please...
```

**Direct:**
```
Help me with: [question]
```

**Wasted tokens:** 30-50 per interaction

### 2. Redundant Confirmation Requests

**Wasteful:**
```
Write a function to parse JSON. Make sure it handles errors. Double-check
that it works correctly. Verify the output is valid.
```

**Sufficient:**
```
Write a JSON parser function with error handling.
```

**Note:** LLMs will naturally handle correctness without being asked repeatedly.

### 3. Over-Explaining the Task

**Wasteful:**
```
I have a list of numbers. This list contains integers. Some numbers might be
negative. Some might be positive. Some might be zero. I want to find all the
numbers that are greater than 10. These are the numbers I'm interested in.
Can you filter the list?
```

**Sufficient:**
```
Filter this list to keep only numbers > 10: [list]
```

### 4. Repeating Context in Follow-ups

**Turn 1:** "Write a User class with name and email properties."

**Turn 2 (wasteful):** "In the User class we created that has name and email
properties, add an age property."

**Turn 2 (efficient):** "Add an age property to the User class."

### 5. Asking for Unnecessary Explanations

**Wasteful:**
```
Write a sort function and explain every line of code in detail and why you
chose this approach and what alternatives exist.
```

**Efficient:**
```
Write a sort function.
```

**Rule:** Only ask for explanations when you need them.

## Context Management Strategies

### 1. Summarize Before Context Grows

When conversation exceeds ~20 turns:
- Summarize key decisions made
- Note active file paths
- List pending tasks
- Clear intermediate artifacts

### 2. Use Clear Section Markers

```
## Task
Build an authentication system

## Constraints
- JWT tokens
- 1-hour expiry
- Refresh tokens

## Files to modify
- auth.py
- config.yaml
```

### 3. Front-Load Important Information

Put critical details at the start of your prompt:
```
[CRITICAL] Database is PostgreSQL 14, not MySQL.

Now, write the migration script...
```

### 4. Batch Related Requests

**Inefficient (3 separate prompts):**
1. "Create a User model"
2. "Create a Post model"
3. "Create a Comment model"

**Efficient (1 prompt):**
```
Create these SQLAlchemy models:
1. User (id, name, email)
2. Post (id, title, body, user_id FK)
3. Comment (id, text, post_id FK, user_id FK)
```

## Few-Shot Example Optimization

### When to Use Few-Shot

- Complex formatting requirements
- Domain-specific conventions
- Consistent output structure needed

### Optimal Example Count

| Task Complexity | Examples Needed |
|-----------------|-----------------|
| Simple format   | 1               |
| Moderate logic  | 2               |
| Complex rules   | 3               |

**More than 3 examples rarely improves quality but always costs tokens.**

### Example Efficiency

**Verbose example:**
```
Example 1:
Input: The user provided "hello world" as their input text.
Output: The resulting transformation of the input is "HELLO WORLD" which is
the uppercase version.
```

**Efficient example:**
```
Example: "hello world" → "HELLO WORLD"
```

### Template Pattern

For repeated tasks, define a template once:

```
Convert to this format:
{name} | {age} | {city}

Example: "John, 30, NYC" → "John | 30 | NYC"

Now convert: [inputs]
```

## Token Estimation Quick Reference

| Content Type | Chars per Token |
|--------------|-----------------|
| English prose | 4.0 |
| Code | 3.5 |
| JSON/YAML | 3.8 |
| URLs/paths | 3.0 |
| Numbers | 2.5 |

### Quick Estimates

- 1 paragraph (~500 chars) ≈ 125 tokens
- 1 function (~20 lines) ≈ 150 tokens
- 1 page of text ≈ 400 tokens
- Code file (~100 lines) ≈ 700 tokens

## Cost-Aware Patterns

### High-Token Operations (Use Sparingly)
- "Explain everything about X"
- "Generate comprehensive documentation"
- "List all possible cases"
- Large code refactoring requests

### Low-Token Operations (Prefer These)
- Targeted questions
- Specific code changes
- Constrained outputs
- Incremental modifications

### Cost Comparison (Claude Sonnet 4)

| Operation | Est. Tokens | Est. Cost |
|-----------|-------------|-----------|
| Simple question | 500 | $0.009 |
| Code review (100 lines) | 2,000 | $0.036 |
| Full file generation | 5,000 | $0.090 |
| Complex refactor | 10,000+ | $0.180+ |

## Summary Checklist

Before sending a prompt, verify:

- [ ] No unnecessary politeness or filler
- [ ] Context isn't repeated from earlier turns
- [ ] Output format/length is specified
- [ ] Request is as specific as possible
- [ ] Few-shot examples are minimal but sufficient
- [ ] Related requests are batched together
- [ ] Only asking for explanations when needed
