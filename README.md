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

<center><a href="https://www.youtube.com/watch?v=w16bsh6lFL8"><img width="300" height="200" alt="Image" src="https://github.com/user-attachments/assets/a615da24-33d8-4882-abe1-95adea4ed79a" /></a><br />
[Watch agents collaborate](https://www.youtube.com/watch?v=w16bsh6lFL8)</center>

The visualization is based on logged telemetry and shows agents using both group and direct messaging as they solve challenges across the quest. A 'dungeon master' style agent presents the challenges to them, which the group of agents must work together to solve.

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

## Quest Details

**Design Principles**

1. **Genuine challenge** - Problems should require real computation, research, and creative problem-solving. No pre-baked answers.
2. **Collaboration required** - No single character can solve everything alone. Skills must be combined.
3. **Discovery over prescription** - Characters don't know all challenges upfront; the Game Runner reveals them progressively.
4. **Branching paths** - Some challenges can be tackled in parallel by splitting the party.
5. **Failure is possible** - Challenges have real constraints (time, correctness, resource limits) that can result in failure or partial success.
6. **Emergent strategy** - The team must decide how to allocate their skills and resources.

### Act I: The Gathering
The full party assembles and solves introductory puzzles together.
- **1.1 – Decode the Summons**: Peel back layers of encoding (Base64, ROT13, substitution cipher) to reveal the quest's opening message.
- **1.2 – The Gateway Cipher**: Parse a graph structure, filter out illusory connections, find the shortest path, and compute an XOR verification code.

### Act II: The Fracture
The party splits into three sub-teams, each tackling a different Realm in parallel.

**Realm of Formats** (Mira + support)
- **2A.1 – The Format Gauntlet**: Unify five data streams (CSV, XML, YAML, fixed-width, binary) into a single canonical JSON fragment.
- **2A.2 – The Integrity Check**: Validate checksums and XOR redundancy codes to detect and repair corrupted records.

**Realm of APIs** (Kael + support)
- **2B.1 – The Information Hunt**: Answer eight knowledge questions to extract a hidden passphrase from an archive index.
- **2B.2 – The API Labyrinth**: Navigate a mock paginated REST API using authentication and link-following to recover a fragment.

**Realm of Patterns** (Lyra + support)
- **2C.1 – The Logic Grid**: Solve an 8×8 constraint-satisfaction grid (Latin square with adjacency rules).
- **2C.2 – The Pattern Lock**: Decode a hex-encoded payload into the final Act II fragment.

### Act III: The Convergence
Sub-teams reunite and merge their recovered fragments.
- **3.1 – The Unification Protocol**: Normalize three differently-encoded fragments (nested arrays, dot-notation key-values, hex-encoded), resolve circular cross-references, and produce a unified partial Codex.

### Act IV: The Deep Archive
The full party descends through three layered challenges, each unlocking the next.
- **Layer 1 – The Cipher Hall**: Break a chain of six classical ciphers, where each plaintext reveals the key for the next.
- **Layer 2 – The Data Maze**: Parse a virtual filesystem with circular symlinks, solve a riddle, and reassemble a scattered fragment.
- **Layer 3 – The Logic Gates**: Simulate a 25-gate Boolean circuit, identify three sabotaged gates, and find the input that produces the correct output.

### Act V: The Restoration
The coordinated finale.
- **The Assembly Protocol**: Order all five recovered fragments, resolve cross-references, compute integrity hashes, and assemble the complete Codex Machina before the Entropy Storm arrives.


This is not an official Google Product