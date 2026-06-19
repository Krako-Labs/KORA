# Goal 093A Metadata Change Approval Packet

Current public HEAD: `7e568a0d8ea7056796bfd8a67bfc7c7cd19f8f9c`

Status: approval packet only. This goal did not change repository settings, update repository description, update topics, update homepage, move files, merge a pull request, create a release, create a tag, create a publication, or change product claims.

## Purpose

KORA's README and documentation now position the project as an AI Workload Control Layer. The public repository metadata still uses older Inference Operating System wording. This packet prepares the exact metadata update for owner approval before any settings are changed.

## Current Repository Metadata

| Field | Current value |
| --- | --- |
| Visibility | `public` |
| Default branch | `main` |
| Description | `An Inference Operating System that reduces unnecessary LLM calls by structuring intelligence before scaling it.` |
| Homepage | empty |
| Topics | `agent-framework`, `ai-infrastructure`, `cost-optimization`, `inference`, `json-schema`, `large-language-models`, `llm`, `open-source`, `orchestration`, `task-graph` |

## Proposed Repository Metadata

| Field | Proposed value |
| --- | --- |
| Description | `AI Workload Control Layer for routing deterministic, reusable, retrieval-needed, tool-needed, and provider-needed work before model invocation.` |
| Homepage | no change |
| Topics | `ai-infrastructure`, `workload-routing`, `ai-workload-control`, `task-graph`, `deterministic-routing`, `llm-infrastructure`, `retrieval-routing`, `tool-routing`, `python`, `open-source` |

## Before And After

| Field | Before | After |
| --- | --- | --- |
| Description | `An Inference Operating System that reduces unnecessary LLM calls by structuring intelligence before scaling it.` | `AI Workload Control Layer for routing deterministic, reusable, retrieval-needed, tool-needed, and provider-needed work before model invocation.` |
| Homepage | empty | no change |
| Topics | `agent-framework`, `ai-infrastructure`, `cost-optimization`, `inference`, `json-schema`, `large-language-models`, `llm`, `open-source`, `orchestration`, `task-graph` | `ai-infrastructure`, `workload-routing`, `ai-workload-control`, `task-graph`, `deterministic-routing`, `llm-infrastructure`, `retrieval-routing`, `tool-routing`, `python`, `open-source` |

## Apply Commands For Later Approval

Do not run these commands until Goal 093B receives explicit owner approval.

Description update:

```bash
GH_CONFIG_DIR="$HOME/.config/gh-hkalbertkim" gh api \
  -X PATCH repos/Krako-Labs/KORA \
  -f description='AI Workload Control Layer for routing deterministic, reusable, retrieval-needed, tool-needed, and provider-needed work before model invocation.'
```

Topics update:

```bash
GH_CONFIG_DIR="$HOME/.config/gh-hkalbertkim" gh api \
  -X PUT repos/Krako-Labs/KORA/topics \
  -H 'Accept: application/vnd.github+json' \
  -f names[]=ai-infrastructure \
  -f names[]=workload-routing \
  -f names[]=ai-workload-control \
  -f names[]=task-graph \
  -f names[]=deterministic-routing \
  -f names[]=llm-infrastructure \
  -f names[]=retrieval-routing \
  -f names[]=tool-routing \
  -f names[]=python \
  -f names[]=open-source
```

Read-back verification after a later approved update:

```bash
GH_CONFIG_DIR="$HOME/.config/gh-hkalbertkim" gh api repos/Krako-Labs/KORA \
  -q '{description:.description,homepage:.homepage,topics:.topics,visibility:.visibility,default_branch:.default_branch}'
```

## Rollback Plan

If the approved metadata update needs to be reverted, restore the current description and topics with these values:

- description: `An Inference Operating System that reduces unnecessary LLM calls by structuring intelligence before scaling it.`
- homepage: empty
- topics: `agent-framework`, `ai-infrastructure`, `cost-optimization`, `inference`, `json-schema`, `large-language-models`, `llm`, `open-source`, `orchestration`, `task-graph`

Rollback commands:

```bash
GH_CONFIG_DIR="$HOME/.config/gh-hkalbertkim" gh api \
  -X PATCH repos/Krako-Labs/KORA \
  -f description='An Inference Operating System that reduces unnecessary LLM calls by structuring intelligence before scaling it.'

GH_CONFIG_DIR="$HOME/.config/gh-hkalbertkim" gh api \
  -X PUT repos/Krako-Labs/KORA/topics \
  -H 'Accept: application/vnd.github+json' \
  -f names[]=agent-framework \
  -f names[]=ai-infrastructure \
  -f names[]=cost-optimization \
  -f names[]=inference \
  -f names[]=json-schema \
  -f names[]=large-language-models \
  -f names[]=llm \
  -f names[]=open-source \
  -f names[]=orchestration \
  -f names[]=task-graph
```

## Risks

- Metadata changes are immediately public in the repository About panel.
- Topic changes may affect discovery and external expectations.
- The proposed wording is clearer but less cost-optimization-centered than the current description.
- The description still mentions model invocation, so future public copy should keep claim boundaries clear.
- Topics should not imply production readiness, package publication, or broad benchmark superiority.

## Confirmation

- No repository settings were changed in Goal 093A.
- No description update was applied.
- No topics update was applied.
- No homepage update was applied.
- No file moves were made.
- No release, tag, publication, or merge was created.

## Recommended Next Goal

Goal 093B - Apply metadata update after explicit owner approval.

Required owner approval sentence:

`Approved: Goal 093B may update the KORA GitHub repository description and topics exactly as specified in docs/reports/goal093a_metadata_change_approval_packet.md.`
