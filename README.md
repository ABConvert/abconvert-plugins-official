# ABConvert Plugins Marketplace

Official Claude Code plugin marketplace by [ABConvert](https://github.com/ABConvert).

## Installation

### 1. Add the marketplace

```bash
claude plugin marketplace add abconvert/abconvert-plugins-official
```

### 2. Install plugins

```bash
claude plugin install ralph-wiggum@abconvert-plugins
```

---

## Available Plugins

### Ralph Wiggum

An iterative development loop that runs Claude with the same prompt repeatedly until task completion. Based on the [Ralph Wiggum technique](https://github.com/anthropics/claude-code/tree/main/plugins/ralph-wiggum) pioneered by Geoffrey Huntley.

**How it works:**
1. You provide a prompt and completion criteria
2. Claude works on the task and attempts to exit
3. A stop hook feeds the same prompt back
4. Claude sees its previous work in files/git history
5. Loop continues until the task is genuinely complete

**Best for:**
- Well-defined tasks with clear success criteria
- Tasks requiring iteration and refinement
- Greenfield projects you can walk away from
- Tasks with automatic verification (tests, linters)

**Not recommended for:**
- Tasks requiring human judgment
- One-shot operations
- Unclear success criteria

### Commands

| Command | Description |
|---------|-------------|
| `/ralph-wiggum:help` | Show help documentation |
| `/ralph-wiggum:ralph-loop` | Start a Ralph loop |
| `/ralph-wiggum:cancel-ralph` | Cancel an active loop |

### Usage Examples

```bash
# Basic loop with iteration limit
/ralph-wiggum:ralph-loop "Build a REST API for todos" --max-iterations 20

# Loop with completion promise
/ralph-wiggum:ralph-loop "Fix all TypeScript errors" --completion-promise "All tests passing"

# Combined options
/ralph-wiggum:ralph-loop "Refactor auth module" --max-iterations 50 --completion-promise "DONE"

# Cancel an active loop
/ralph-wiggum:cancel-ralph
```

### Completion Promise

To exit the loop, Claude must output the exact promise text in XML tags:

```
<promise>YOUR_PROMISE_TEXT</promise>
```

The promise must be **genuinely true** - Claude cannot lie to escape the loop.

---

## Uninstall

```bash
# Remove a plugin
claude plugin uninstall ralph-wiggum@abconvert-plugins

# Remove the marketplace
claude plugin marketplace remove abconvert-plugins
```

---

## Bug Fixes

This version includes fixes from [PR #12642](https://github.com/anthropics/claude-code/pull/12642) addressing [issue #12170](https://github.com/anthropics/claude-code/issues/12170):

- Fixed multi-line bash command blocking by security check
- Fixed permission check bug with auto-execute syntax
- Added clearer completion promise instructions

---

## Contributing

Issues and pull requests welcome at [github.com/abconvert/abconvert-plugins-official](https://github.com/abconvert/abconvert-plugins-official).

## License

MIT

## Credits

- Original Ralph Wiggum technique by [Geoffrey Huntley](https://github.com/ghuntley)
- Original plugin by [Daisy Hollman](https://github.com/anthropics/claude-code/tree/main/plugins/ralph-wiggum) at Anthropic
- Bug fixes from [PR #12642](https://github.com/anthropics/claude-code/pull/12642)
