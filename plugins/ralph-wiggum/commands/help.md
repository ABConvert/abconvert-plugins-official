---
description: "Show Ralph Wiggum help and documentation"
---

# Ralph Wiggum Plugin Help

## What is the Ralph Wiggum Technique?

The Ralph Wiggum technique is an iterative development methodology based on continuous AI loops, pioneered by Geoffrey Huntley. Rather than feeding output back as input, the approach works by repeatedly providing the same prompt while Claude observes its previous modifications in files and git history.

Each cycle follows this pattern:
1. Claude receives an identical prompt
2. Makes file modifications toward the goal
3. Attempts to exit
4. A stop hook reintroduces the same prompt
5. Claude reviews prior iterations in the codebase
6. Continues refining until task completion

The methodology operates as "deterministically bad in an undeterministic world" - failures become predictable, allowing systematic improvement through prompt refinement.

## Available Commands

**`/ralph-loop <PROMPT> [OPTIONS]`** - Initiates a Ralph loop in your current session with options for `--max-iterations <n>` and `--completion-promise <text>`.

**`/cancel-ralph`** - Terminates an active loop by removing the state file and reporting iteration count.

## Key Mechanisms

Completion requires outputting: `<promise>YOUR_PROMISE_TEXT</promise>`

## When to Use Ralph

**Good for:**
- Well-defined tasks with clear success criteria
- Tasks requiring iteration and refinement
- Greenfield projects where you can walk away
- Tasks with automatic verification (tests, linters)

**Not good for:**
- Tasks requiring human judgment
- One-shot operations
- Tasks with unclear success criteria
- Production debugging

## Examples

```bash
# Simple loop with iteration limit
/ralph-loop "Build a REST API for todos" --max-iterations 20

# Loop with completion promise
/ralph-loop "Fix all TypeScript errors" --completion-promise "All tests passing"

# Combined options
/ralph-loop "Refactor auth module" --max-iterations 50 --completion-promise "DONE"
```
