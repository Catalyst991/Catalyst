# CLAUDE.md

## Agent skills

### Issue tracker

Issues and PRDs live as GitHub issues in `Catalyst991/Catalyst`, managed via the `gh` CLI. See [docs/agents/issue-tracker.md](docs/agents/issue-tracker.md).

### Triage labels

Default label names used for each triage state role, plus the `epic` structural marker. See [docs/agents/triage-labels.md](docs/agents/triage-labels.md).

### Domain docs

Single-context layout: one `CONTEXT.md` + `docs/adr/` at the repo root. See [docs/agents/domain.md](docs/agents/domain.md).

### Agent brief

The shared spec format both `to-issues` and `triage` use to write work for AFK agents. See [docs/agents/agent-brief.md](docs/agents/agent-brief.md).

### Handoffs

In-flight session context written by `/handoff-conversation` lives in `docs/agents/handoffs/`. When resuming a session, read the most recent file in that folder before doing anything else.
