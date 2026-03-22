# Relics of the Athenaeum

<img width="1280" height="714" alt="Image" src="https://github.com/user-attachments/assets/cbee74a3-f3aa-4739-b423-0a83d5dd4c13" />

A multi-agent collaborative quest game that demonstrates autonomous agent orchestration using Scion. Five AI characters with distinct specializations work together - guided by a Game Runner (Dungeon Master) agent - to solve computational challenges, recover lost knowledge fragments, and restore an ancient artifact.

## What This Demonstrates

- **Multi-vendor agent collaboration**: Characters run on different AI models (Gemini, Claude, GPT) through different harnesses, working together seamlessly
- **Autonomous CLI discovery**: Agents learn and use the `scion` CLI dynamically to communicate, spawn helpers, and coordinate
- **Hierarchical agent spawning**: The Game Runner spawns characters, characters request sprite workers, and peripheral agents (Oracle, Healer) are summoned on demand
- **File-based coordination**: Agents share a workspace, reading challenge data and writing solutions to agreed locations
- **Message-based communication**: Real-time coordination via direct messages and party-wide broadcasts
- **Resource management**: Limited Oracle/Healer summons and sprite slots create strategic trade-offs

## The Cast

### Main Characters
| Character | Role | Harness | Model |
|-----------|------|---------|-------|
| **Game Runner** | Dungeon Master / Orchestrator | gemini | gemini-3.1-pro-preview |
| **Lyra the Logician** | Algorithms & code | gemini | gemini-3.1-pro-preview |
| **Kael the Chronicler** | Research & information | gemini | gemini-3-flash-preview |
| **Mira the Mapper** | Data transformation | gemini | gemini-3-flash-preview |
| **Thorne the Sentinel** | Validation & testing | claude | claude-opus-4-6 |
| **Zara the Weaver** | Integration & orchestration | claude | claude-sonnet-4-6 |

### Peripheral Characters
| Character | Role | Harness | Model | Notes |
|-----------|------|---------|-------|-------|
| **The Oracle** | Deep domain knowledge | codex | gpt-5.4 | Summoned on demand, single-use |
| **The Healer** | Debugging & error recovery | claude | claude-sonnet-4-6 | Summoned on demand, single-use |
| **The Scribe** | Quest state recorder | gemini | gemini-3-flash-preview | Background/detached process |

### Sprites (Ephemeral Workers)
| Sprite | Summoner | Purpose | Model |
|--------|----------|---------|-------|
| Calculus Sprite | Lyra | Computational sub-tasks | gemini-3-flash-preview |
| Seeker Wisp | Kael | Research sub-tasks | gemini-3-flash-preview |
| Flux Mote | Mira | Data transformations | gemini-3-flash-preview |
| Ward Echo | Thorne | Parallel test execution | claude-sonnet-4-6 |
| Thread Sprite | Zara | Integration tasks | gemini-3-flash-preview |

## Quest Structure

```
Act I: The Gathering        - Party assembles, solves initial puzzles together
Act II: The Fracture         - Party splits into 3 sub-teams for parallel challenges
Act III: The Convergence     - Sub-teams reunite, unify recovered fragments
Act IV: The Deep Archive     - Full party descends through 3 layered challenges
Act V: The Restoration       - Coordinated finale to reassemble the Codex
```

## Setup

### Prerequisites

- Scion CLI installed
- A running Scion server with hub enabled
- API keys configured for the harnesses you want to use (gemini, claude, codex)

### Initialize the Grove

From this directory:

```bash
scion init
```

### Sync Templates to Hub

Start the server and link the grove:

```bash
scion server start
scion config set hub.endpoint http://localhost:8080
scion hub enable
scion hub link
```

This will detect the templates in `.scion/templates/` and prompt you to sync them to the hub.

### Start the Game

Launch the Game Runner agent:

```bash
scion start game-runner --type game-runner
```

The Game Runner will autonomously:
1. Spawn all 5 main characters and the Scribe
2. Set up the shared workspace directory structure
3. Broadcast the opening narrative
4. Deploy the first challenge

From there, the agents collaborate autonomously. You can observe via:

```bash
# See all running agents
scion list

# Watch a specific agent's activity
scion look game-runner
scion look lyra

# Attach to an agent for direct interaction
scion attach game-runner
```

## Project Structure

```
.
├── README.md                    # This file
├── .design/                     # Design documents
│   ├── game-plan.md             # High-level quest design
│   ├── characters.md            # Character definitions
│   ├── quest-scenario.md        # Full quest scenario and challenges
│   ├── game-mechanics.md        # Rules, communication, orchestration
│   └── scion-templates.md       # Template specifications
└── .scion/
    └── templates/               # Scion agent templates
        ├── game-runner/         # DM / orchestrator (includes home/playbook/)
        ├── lyra/                # Algorithmic problem solver
        ├── kael/                # Researcher
        ├── mira/                # Data transformer
        ├── thorne/              # Validator / tester
        ├── zara/                # Integrator / orchestrator
        ├── oracle/              # Domain knowledge expert (summoned)
        ├── healer/              # Debugger (summoned)
        ├── scribe/              # Background recorder
        ├── calculus-sprite/     # Computational worker
        ├── seeker-wisp/         # Research worker
        ├── flux-mote/           # Transformation worker
        ├── ward-echo/           # Validation worker
        └── thread-sprite/       # Integration worker
```

## What's Still Needed

The templates define the agents and their roles. To actually run the game, you'll also need:

- **Playbook data**: The challenge files, encoded puzzles, data files, and solution keys that go in `game-runner/home/playbook/`. These are the actual puzzles the agents solve.
- **Harness configuration**: API keys and harness configs for gemini, claude, and codex.
