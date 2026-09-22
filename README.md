# ABConvert Plugins

Skills and plugins by [ABConvert](https://github.com/ABConvert). Each skill is a standard `SKILL.md` folder, so it runs in Claude, Claude Code, ChatGPT, and Codex.

| Skill | Use it when |
|---|---|
| [Shopify Insight Report](#shopify-insight-report) | A Shopify store's conversion, sales, or traffic changed and nobody knows why |
| [Ralph Wiggum](#ralph-wiggum) | You want Claude Code to loop on a task until it is genuinely done |

## Shopify Insight Report

A merchant, a prospect, or your own client says "CVR dropped 30% this month and we can't figure out why", or "sales have been down since we published the new theme". This skill answers with the store's own Shopify analytics: it finds the day and hour the metric broke, which funnel step and segment moved, and whether the suspected change could have caused it. Any change can be the suspect: theme, app, checkout, shipping, price, discount, campaign, migration, or A/B test.

The output is a one-page HTML report. Three conclusions at the top, a timeline, and one chart per question with the ShopifyQL query beside it, so the merchant can re-run every number in Shopify Analytics.

```
Our conversion rate dropped about 30% over the last month and nobody knows why.
Can you look at the store and tell me what happened?
```

**Docs.** The skill links Shopify's official ShopifyQL pages for every dataset and clause and reads those, rather than a paraphrase.

**Store access, one of three.** A Shopify MCP connected to the store (Shopify's official Claude and ChatGPT connectors work, and an agency's collaborator account with only Reports and Dashboards permissions is enough). Or a read-only Admin API token, which the bundled script refuses to use if it carries any write scope. Or CSV exports the merchant makes from Shopify's ShopifyQL editor, for clients with no network. The skill never runs a mutation on any path. On the token path the secret stays out of the chat: set `SHOPIFY_ACCESS_TOKEN_CMD` to a password-manager or keychain lookup and the script fetches it itself, or export the token in your terminal before starting the agent.

### Install

**Claude Code**

```bash
claude plugin marketplace add ABConvert/abconvert-plugins-official
claude plugin install shopify-insight-report@abconvert-plugins
```

Add `--scope project` to limit it to the current repo. This is the only client that also gets the plugin's hook, which blocks any shell command carrying a GraphQL mutation to a Shopify Admin API. Without the marketplace, the open-source [skills CLI](https://github.com/vercel-labs/skills) installs the skill alone:

```bash
npx skills add ABConvert/abconvert-plugins-official --skill shopify-insight-report -a claude-code
```

**Claude (claude.ai)**

Download [shopify-insight-report.zip](https://github.com/ABConvert/abconvert-plugins-official/releases/latest/download/shopify-insight-report.zip) from the latest release and upload it under Skills, Create skill. Needs a plan with code execution enabled. [Help article.](https://support.claude.com/en/articles/12512198-how-to-create-custom-skills) On a Team or Enterprise plan, one person uploads it and then shares it with colleagues or publishes it to the organisation's skills directory.

**ChatGPT**

Same zip. Upload it under Skills, Create, Upload from your computer, then @-mention `shopify-insight-report` in a chat or add it to a Project. ChatGPT reads the same `SKILL.md` format. [Help article.](https://help.openai.com/en/articles/20001066-skills-in-chatgpt) ChatGPT's sandbox has no outbound network, so use the connector or the CSV path there. Workspace admins can publish it to the whole workspace.

**Codex**

```bash
npx skills add ABConvert/abconvert-plugins-official --skill shopify-insight-report -a codex
```

Or copy the folder into `~/.codex/skills/` by hand, or into `.agents/skills/` inside a repo to share it with that repo's collaborators. It shows up in `/skills` without a restart.

**Building the zip yourself** (for a branch that has no release yet):

```bash
git clone https://github.com/ABConvert/abconvert-plugins-official
cd abconvert-plugins-official/plugins/shopify-insight-report/skills
zip -r shopify-insight-report.zip shopify-insight-report
```

## Ralph Wiggum

Runs Claude Code on the same prompt repeatedly until the task is genuinely complete: a stop hook feeds the prompt back, and Claude sees its own previous work in the files and git history. Best for well-defined tasks with automatic verification, such as "fix all TypeScript errors". Details, options, and the completion-promise mechanism are in [the plugin's README](plugins/ralph-wiggum/README.md).

```bash
claude plugin marketplace add ABConvert/abconvert-plugins-official
claude plugin install ralph-wiggum@abconvert-plugins
```

| Command | Description |
|---|---|
| `/ralph-wiggum:ralph-loop "<prompt>" --max-iterations 20` | Start a loop |
| `/ralph-wiggum:cancel-ralph` | Cancel the active loop |
| `/ralph-wiggum:help` | Show help |

This copy carries the fixes from [anthropics/claude-code#12642](https://github.com/anthropics/claude-code/pull/12642) for [issue #12170](https://github.com/anthropics/claude-code/issues/12170).

## Uninstall

```bash
claude plugin uninstall shopify-insight-report@abconvert-plugins
claude plugin uninstall ralph-wiggum@abconvert-plugins
claude plugin marketplace remove abconvert-plugins
```

For Claude, ChatGPT, and Codex, delete the skill from the Skills page or the skills directory.

## Contributing

Issues and pull requests welcome at [github.com/ABConvert/abconvert-plugins-official](https://github.com/ABConvert/abconvert-plugins-official). To cut a release, push a tag such as `v1.1.0`; the release workflow zips every skill folder and attaches the zips to the GitHub release.

## License

MIT

## Credits

- Original Ralph Wiggum technique by [Geoffrey Huntley](https://github.com/ghuntley)
- Original plugin by [Daisy Hollman](https://github.com/anthropics/claude-code/tree/main/plugins/ralph-wiggum) at Anthropic
- Bug fixes from [PR #12642](https://github.com/anthropics/claude-code/pull/12642)
