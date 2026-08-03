# Triage Labels

The skills use two kinds of label vocabulary, and this file maps both to the actual label strings used in this repo's issue tracker. Edit the right-hand columns to match whatever vocabulary you actually use.

## Triage state roles

Every *triaged* issue carries exactly one of these five. They describe where an issue sits in the triage state machine — inbound/backlog work flows through them via the `triage` skill.

| Canonical role    | Label in our tracker | Meaning                                  |
| ----------------- | --------------------- | ----------------------------------------- |
| `needs-triage`    | `needs-triage`         | Maintainer needs to evaluate this issue  |
| `needs-info`      | `needs-info`           | Waiting on reporter for more information |
| `ready-for-agent` | `ready-for-agent`      | Fully specified, ready for an AFK agent  |
| `ready-for-human` | `ready-for-human`      | Requires human implementation            |
| `wontfix`         | `wontfix`              | Will not be actioned                     |

## Structural markers

These are **not** triage states. They mark an issue's structural role so the pipeline can tell planning artifacts apart from buildable work. An issue may carry one in addition to a state role.

| Canonical marker | Label in our tracker | Meaning                                                                 |
| ----------------- | --------------------- | ----------------------------------------------------------------------- |
| `epic`             | `epic`                 | A PRD / parent issue that `to-issues` decomposes into slices. **Never buildable directly.** Applied by `to-prd`; its child slices reference it as their Parent. |

> An executor must **never** treat an `epic` as `ready-for-agent` — that's the whole reason the marker exists (otherwise an agent tries to build the entire epic in one shot).
>
> Notes on the `epic` marker by tracker:
> - **GitHub / GitLab (free) / most others**: it's a label.
> - **GitLab Premium**: you may map it to a native Epic instead of a label.
> - **Local markdown**: the PRD is a file (`.scratch/<feature>/PRD.md`), so it needs no marker at all — its location already says it's the parent.
> - Alias: some repos prefer `parent`. Pick one string and put it in the right-hand column.

When a skill mentions a role or marker (e.g. "apply the AFK-ready label", "mark the PRD as an epic"), use the corresponding label string from these tables.
