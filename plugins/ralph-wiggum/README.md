# Ralph Wiggum Plugin

An iterative development loop that runs Claude with the same prompt repeatedly until task completion.

## What is the Ralph Wiggum Technique?

The Ralph Wiggum technique is an iterative development methodology based on continuous AI loops, pioneered by [Geoffrey Huntley](https://github.com/ghuntley). Rather than feeding output back as input, the approach works by repeatedly providing the same prompt while Claude observes its previous modifications in files and git history.

**Each cycle follows this pattern:**
1. Claude receives an identical prompt
2. Makes file modifications toward the goal
3. Attempts to exit
4. A stop hook reintroduces the same prompt
5. Claude reviews prior iterations in the codebase
6. Continues refining until task completion

## Installation

```bash
# Add the marketplace (if not already added)
claude plugin marketplace add abconvert/abconvert-plugins-official

# Install the plugin
claude plugin install ralph-wiggum@abconvert-plugins
```

## Commands

| Command | Description |
|---------|-------------|
| `/ralph-wiggum:help` | Show help documentation |
| `/ralph-wiggum:ralph-loop` | Start a Ralph loop |
| `/ralph-wiggum:cancel-ralph` | Cancel an active loop |

## Usage

### Start a Ralph Loop

```bash
/ralph-wiggum:ralph-loop "YOUR_TASK" [OPTIONS]
```

**Options:**
- `--max-iterations <n>` - Maximum iterations before auto-stop (default: unlimited)
- `--completion-promise '<text>'` - Promise phrase to signal completion

### Examples

```bash
# Basic loop with iteration limit
/ralph-wiggum:ralph-loop "Build a REST API for todos" --max-iterations 20

# Loop with completion promise
/ralph-wiggum:ralph-loop "Fix all TypeScript errors" --completion-promise "All tests passing"

# Combined options
/ralph-wiggum:ralph-loop "Refactor auth module" --max-iterations 50 --completion-promise "DONE"
```

### Cancel a Loop

```bash
/ralph-wiggum:cancel-ralph
```

## Completion Promise

To exit the loop, Claude must output the exact promise text in XML tags:

```
<promise>YOUR_PROMISE_TEXT</promise>
```

**Important:** The promise must be genuinely true. Claude cannot lie to escape the loop - the loop is designed to continue until the task is actually complete.

## When to Use Ralph

**Best for:**
- Well-defined tasks with clear success criteria
- Tasks requiring iteration and refinement
- Greenfield projects you can walk away from
- Tasks with automatic verification (tests, linters)

**Not recommended for:**
- Tasks requiring human judgment
- One-shot operations
- Tasks with unclear success criteria
- Production debugging

## Monitoring

```bash
# View current iteration
grep '^iteration:' .claude/ralph-loop.local.md

# View full state
head -10 .claude/ralph-loop.local.md
```

## Bug Fixes

This version includes fixes from [PR #12642](https://github.com/anthropics/claude-code/pull/12642):

- Fixed multi-line bash command blocking by security check
- Fixed permission check bug with auto-execute syntax
- Added clearer completion promise instructions

## Credits

- Original technique by [Geoffrey Huntley](https://github.com/ghuntley)
- Original plugin by [Daisy Hollman](https://github.com/anthropics/claude-code/tree/main/plugins/ralph-wiggum) at Anthropic
