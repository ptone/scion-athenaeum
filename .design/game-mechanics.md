# Game Mechanics & Process: The Shattered Codex

This document describes how the game actually runs: how the Game Runner orchestrates play, how agents communicate, how challenges are revealed, and how agents are directed and coordinated using scion primitives.

## 1. Scion Primitives Used

The game relies on these scion capabilities:

### Agent Lifecycle
- `scion start <name> --type <template> [task...]` - Game Runner spawns character agents
- `scion create <name> --type <template>` + `scion start <name>` - Two-step spawn for pre-configured agents
- `scion stop <name>` - Stop an agent (sprite cleanup, etc.)
- `scion look <name>` - Game Runner inspects what an agent is currently doing
- `scion list` - Game Runner checks status of all agents

### Messaging
- `scion message <agent> "<text>"` - Direct message to a specific agent
- `scion msg <agent> "<text>"` - Same (alias)
- `scion message --broadcast "<text>"` - Send message to ALL running agents in the grove (the group chat)
- `scion message <agent> --interrupt "<text>"` - Urgent message that interrupts the agent's current work
- `scion message <agent> --attach path/to/file.md` - Send a message with a file attachment reference
- `scion message --broadcast --attach challenges/act-1/data.json "New challenge data available"` - Broadcast with attachment

Messages arrive in the agent's conversation as structured JSON blocks delimited by `---BEGIN SCION MESSAGE---` / `---END SCION MESSAGE---`, including sender identity (`agent:<name>` or `user:<name>`), type, and broadcast flag.

### Notifications
- `scion start <name> --notify` / `scion msg <name> --notify` - Subscribe to status changes (COMPLETED, WAITING_FOR_INPUT)
- Game Runner uses `--notify` when starting agents so it learns when they finish or need help

### Agent Home Directory
- Each template's `home/` folder is mounted into the agent container as its home directory
- Files in `home/` are private to that agent - other agents cannot see them
- The Game Runner template's `home/` contains the hidden challenge playbook files

### Shared Workspace
- All agents share the same git repository workspace mounted at `/workspace`
- Files written to the workspace are visible to all agents
- This is the primary coordination surface alongside messaging

## 2. Game Runner's Hidden Playbook

The Game Runner's template includes a `home/` directory containing the complete quest playbook - challenge definitions, solution keys, data files, and progression logic. These files are **invisible to all other agents** because they live in the Game Runner's private agent-home, not in the shared workspace.

### Game Runner Template Home Structure

```
game-runner/
├── scion-agent.yaml
├── agents.md
├── system-prompt.md
└── home/
    └── playbook/
        ├── README.md                    # Game Runner's master guide
        ├── act-1/
        │   ├── challenge-1.1.md         # Challenge description, hints, solution key
        │   ├── challenge-1.2.md
        │   ├── data/
        │   │   ├── summons.txt          # Encoded summons file (deploy to workspace)
        │   │   └── gateway-data.json    # Graph data (deploy to workspace)
        │   └── solutions/
        │       ├── summons-decoded.txt  # Expected decoded output
        │       └── gateway-answer.txt   # Expected XOR value
        ├── act-2a/
        │   ├── challenge-2a.1.md
        │   ├── challenge-2a.2.md
        │   ├── data/
        │   │   ├── fragment-csv.csv
        │   │   ├── fragment-xml.xml
        │   │   ├── fragment-yaml.yaml
        │   │   ├── fragment-fixed.txt
        │   │   └── fragment-binary.b64
        │   └── solutions/
        │       └── unified-fragment-a.json
        ├── act-2b/
        │   └── ...
        ├── act-2c/
        │   └── ...
        ├── act-3/
        │   └── ...
        ├── act-4/
        │   └── ...
        └── act-5/
            └── ...
```

### Progressive Revelation Process

The Game Runner reveals challenges by **copying files from its private home directory into the shared workspace**:

```bash
# Game Runner copies challenge data into workspace when it's time
cp ~/playbook/act-1/data/summons.txt /workspace/challenges/act-1/summons.txt
```

Then broadcasts that the challenge is available:

```bash
scion message --broadcast "The ancient summons has appeared in challenges/act-1/summons.txt. Your quest begins - decode its message to learn your mission."
```

The Game Runner also writes a `current-challenge.md` to the workspace with narrative framing and any rules specific to this challenge.

### Challenge File Format

Each challenge markdown in the playbook follows a standard structure:

```markdown
# Challenge 1.1: Decode the Summons

## Narrative
[Flavor text the Game Runner can use or adapt when presenting the challenge]

## Setup
[Instructions for the Game Runner on what to deploy and how]
- Copy `data/summons.txt` to `/workspace/challenges/act-1/`
- Write challenge description to `/workspace/current-challenge.md`

## Solution Key
[What the correct answer looks like - used by Game Runner to validate]
- Decoded text: "The Codex Machina lies shattered across five realms..."
- Key validation: decoded output contains the phrase "five fragments"

## Hints (Escalating)
1. "The outer layer is a common encoding used in email attachments."
2. "After removing the first layer, the text seems shifted by a familiar number."
3. "The noise in the header comment isn't noise at all - look for pairs of numbers."

## Complications (if too easy)
[Optional twists the Game Runner can add if the team is breezing through]
- Add a second substitution layer using a different key
- Corrupt 3 characters in the base64 encoding

## Acceptance Criteria
- Exact match on decoded message text
- OR functional match: output contains all 5 key phrases
```

## 3. Communication Model

Agents communicate through two channels: **messages** (real-time) and **shared files** (persistent).

### Channel 1: Scion Messages (Real-Time Chat)

Messages are the primary real-time communication channel. They function like a group chat when broadcast, or direct messages when targeted.

**Broadcast (Group Chat):**
Any agent can broadcast to the whole party:
```bash
# An agent sends to all other running agents
scion message --broadcast "I've decoded the first layer - it's base64. The inner text looks like ROT13. Who can help with the substitution cipher?"
```

All running agents receive this as a structured message in their conversation, with the sender identified:
```
---BEGIN SCION MESSAGE---
{
  "version": 1,
  "timestamp": "2026-03-19T14:30:00Z",
  "sender": "agent:lyra",
  "msg": "I've decoded the first layer...",
  "type": "instruction",
  "broadcasted": true
}
---END SCION MESSAGE---
```

**Direct Messages:**
For focused coordination between two agents:
```bash
scion message thorne "Can you validate this decoded output? I've written it to solutions/act-1/decoded-attempt-1.txt"
```

**Game Runner Announcements:**
The Game Runner uses broadcast for scene-setting and challenge reveals, and direct messages for task assignments:
```bash
# Scene setting (broadcast)
scion message --broadcast "The Gateway cipher awaits. A file of tangled connections has materialized at challenges/act-1/gateway-data.json. Find the true shortest path."

# Direct task assignment
scion message lyra "Lyra, implement a shortest-path algorithm for the graph structure. Be wary of edges marked 'illusory' in the metadata."
scion message mira "Mira, parse the gateway-data.json and produce a clean adjacency list. Watch for the nested metadata fields."
```

### Channel 2: Shared Workspace Files (Persistent State)

Files in `/workspace` are visible to all agents and persist across the session. Used for:

- **Challenge data** - `challenges/<act>/` - Game Runner deploys data files here
- **Solutions** - `solutions/<act>/` - Agents write their outputs here
- **Handoffs** - Agents write intermediate artifacts for other agents to pick up
- **Notes** - `notes/` - Agents can write longer-form analysis, plans, or findings

### When to Use Which Channel

| Purpose | Channel | Why |
|---------|---------|-----|
| Quick coordination, questions | Broadcast message | Real-time, everyone sees it |
| Task assignment from Game Runner | Direct message | Targeted, clear ownership |
| Delivering code, data, artifacts | Shared files + message notifying | Files persist, message alerts |
| Strategic discussion | Broadcast message | Group decision-making |
| Game Runner reveals challenge | Broadcast + file deployment | Narrative + data together |
| Solution submission | Write file + message Game Runner | Artifact + notification |

### Communication Conventions

Agents should follow these patterns (established in their `agents.md`):

1. **Announce what you're working on** via broadcast before starting
2. **Announce when you've produced output** with the file path
3. **Ask specific agents by name** when you need their particular skill
4. **Write artifacts to agreed locations** in the workspace, not ad-hoc paths
5. **Read the latest `current-challenge.md`** before starting work on anything new

## 4. Game Runner Orchestration Process

### Phase 0: Game Startup

The Game Runner is the first agent started (by the human operator). Its startup task instructs it to begin the quest:

```bash
# Human operator starts the game
scion start game-runner --type game-runner "Begin The Shattered Codex quest. Start all character agents, set the scene, and deploy Act I Challenge 1.1."
```

The Game Runner then:

1. Creates and starts the 5 main character agents:
```bash
scion start lyra --type lyra --non-interactive --notify
scion start kael --type kael --non-interactive --notify
scion start mira --type mira --non-interactive --notify
scion start thorne --type thorne --non-interactive --notify
scion start zara --type zara --non-interactive --notify
```

2. Starts the Scribe (background recorder):
```bash
scion start scribe --type scribe --non-interactive
```

3. Sets up the workspace directory structure:
```bash
# In workspace
mkdir -p challenges/{act-1,act-2a,act-2b,act-2c,act-3,act-4,act-5}
mkdir -p solutions/{act-1,act-2a,act-2b,act-2c,act-3,act-4,act-5}
mkdir -p inventory notes
```

4. Writes the initial `game-context.md` and `current-challenge.md`

5. Broadcasts the opening scene to all agents

6. Deploys the first challenge data

### Phase 1: Running a Challenge

```
Game Runner                    Character Agents
    │                               │
    ├── Copy data from ~/playbook   │
    │   to /workspace/challenges/   │
    │                               │
    ├── Write current-challenge.md  │
    │                               │
    ├── Broadcast: "New challenge"──┤
    │   (+ direct assignments)      │
    │                               │
    │   ┌───────────────────────────┤
    │   │ Agents discuss strategy   │
    │   │ via broadcasts            │
    │   │                           │
    │   │ Agents work on their      │
    │   │ portions                  │
    │   │                           │
    │   │ Agents write outputs to   │
    │   │ /workspace/solutions/     │
    │   │                           │
    │   │ Agent messages Game Runner│
    │   │ "Solution ready"          │
    │   └───────────────────────────┤
    │                               │
    ├── Read solution from          │
    │   /workspace/solutions/       │
    │                               │
    ├── Compare against             │
    │   ~/playbook/.../solutions/   │
    │                               │
    ├── If correct:                 │
    │   ├── Broadcast "Success!"    │
    │   ├── Update game-context.md  │
    │   └── Advance to next         │
    │                               │
    ├── If incorrect:               │
    │   ├── Message feedback        │
    │   └── Wait for retry          │
    │                               │
```

### Phase 2: Direct Task Assignment

The Game Runner doesn't always leave task allocation to the party. It can directly assign work, especially when:
- The challenge has clear role requirements
- The party is stuck and needs direction
- Time pressure requires efficient allocation
- A specific skill match is obvious

**Assignment patterns:**

```bash
# Clear, direct assignment
scion message lyra "Lyra, your task: Write a BFS shortest-path algorithm for the graph in challenges/act-1/gateway-data.json. Output the path and XOR of node values to solutions/act-1/shortest-path.txt"

# Assignment with collaboration instruction
scion message mira "Mira, parse gateway-data.json into a clean adjacency list format. Write it to solutions/act-1/graph-clean.json. Lyra will need this for her pathfinding work."

# Nudging collaboration
scion message --broadcast "This challenge requires both data parsing AND algorithm work. Mira and Lyra should coordinate. Thorne, prepare validation tests."
```

The Game Runner can also **reassign** if an agent is struggling:
```bash
scion message kael "Kael, Lyra is stuck on identifying the cipher type. Research 16th century polyalphabetic ciphers and share your findings with her."
```

### Phase 3: Spawning Peripheral Agents

When a character requests an Oracle or Healer summon (via broadcast or direct message to Game Runner), the Game Runner spawns the appropriate agent:

```bash
# Oracle summon - the task IS the question
scion start oracle-summon-1 --type oracle --non-interactive --notify "Research and answer this question precisely: What is the atomic number of the element discovered in the year the Eiffel Tower was completed? Provide only the number and your reasoning. Write your answer to /workspace/oracle-responses/response-1.md"

# Healer summon
scion start healer-summon-1 --type healer --non-interactive --notify "Debug and fix the broken code at /workspace/solutions/act-2a/transform.py. The error is: 'KeyError: namespace_uri' when processing the XML fragment. Write the fixed version to the same path."
```

The Game Runner tracks resource usage and enforces limits:
```bash
# If Oracle summons exhausted
scion message lyra "The Oracle cannot be summoned again this act. You have exhausted your summons. You must find another way."
```

### Phase 4: Party Split (Act II)

For parallel work in Act II, the Game Runner:

1. Asks the party to discuss allocation:
```bash
scion message --broadcast "Three realms lie before you. You must split into teams. Discuss among yourselves who goes where, then tell me your decision. The realms: (1) A realm of incompatible forms, (2) A realm of distant knowledge, (3) A realm of logical barriers."
```

2. Waits for the party to decide (monitors broadcasts)

3. Once decided, sends each sub-team their specific challenge:
```bash
# Team A: Realm of Formats
scion message mira "Mira, you lead Team A into the Realm of Formats. Your challenge awaits."
scion message lyra "Lyra, join Mira in the Realm of Formats. She'll need your help with the trickier encodings."

# Deploy Team A's challenge
cp ~/playbook/act-2a/data/* /workspace/challenges/act-2a/
scion message mira "Challenge data deployed to challenges/act-2a/. Five files, five formats, one truth."
scion message lyra "Challenge data deployed to challenges/act-2a/. Five files, five formats, one truth."
```

4. Monitors all three tracks, providing hints as needed

5. When all three complete, triggers convergence:
```bash
scion message --broadcast "All teams have returned. Three fragments recovered. But they speak different languages. Your next challenge: make them speak as one. See current-challenge.md."
```

### Phase 5: Sprite Spawning

When a character wants to spawn a sprite (worker agent), they message the Game Runner or directly use the scion CLI (depending on permissions). The Game Runner approach is preferred for resource tracking:

```bash
# Lyra requests a Calculus Sprite
# (Lyra broadcasts or messages Game Runner)
scion message game-runner "Requesting a Calculus Sprite to brute-force search for prime factors of the node values. Task spec written to /workspace/sprites/calculus-task-1.md"

# Game Runner spawns it
scion start calc-sprite-1 --type calculus-sprite --non-interactive --notify "Execute the task defined in /workspace/sprites/calculus-task-1.md. Write results to /workspace/sprites/calculus-result-1.md"
```

Alternatively, character agents can be given permission in their `agents.md` to spawn their own sprites directly using the scion CLI (since `agents-hub.md` instructs them on CLI usage). The Game Runner would monitor via `scion list`.

## 5. Game State Management

### game-context.md

Maintained by the Scribe agent (or by the Game Runner if no Scribe). Located at `/workspace/game-context.md`.

```markdown
# The Shattered Codex - Game State

## Current Act: I - The Gathering
## Active Challenge: 1.2 - The Gateway Cipher

## Party Formation: Together (all agents)

## Resources
| Resource | Remaining |
|----------|-----------|
| Oracle Summons | 1 |
| Healer Summons | 1 |
| Active Sprites | 0 / 3 max |

## Inventory
| Fragment | Status |
|----------|--------|
| A (Formats) | Not found |
| B (APIs) | Not found |
| C (Patterns) | Not found |
| D (Archive) | Not found |
| E (Archive) | Not found |

## Completed Challenges
- [x] 1.1 Decode the Summons

## Agent Status
| Agent | Status | Working On |
|-------|--------|------------|
| Lyra | Active | Implementing BFS for gateway graph |
| Kael | Active | Researching graph structure properties |
| Mira | Active | Parsing gateway-data.json |
| Thorne | Active | Writing path validation tests |
| Zara | Active | Coordinating solution assembly |
```

### current-challenge.md

Written by the Game Runner at the start of each challenge. Contains narrative + practical information visible to all agents.

```markdown
# Current Challenge: The Gateway Cipher

*The ancient gateway hums with potential energy. Its surface is etched with an intricate web of connected nodes - a map of relationships that must be understood before passage is granted.*

## Objective
Find the shortest path between nodes "ORIGIN" and "TERMINUS" in the graph defined in `challenges/act-1/gateway-data.json`. Compute the XOR of all node values along this path.

## Data
- Input: `challenges/act-1/gateway-data.json`
- Output: Write the answer (single integer) to `solutions/act-1/gateway-answer.txt`
- Also write the path (ordered list of node names) to `solutions/act-1/gateway-path.txt`

## Rules
- The graph may contain misleading connections - verify your assumptions
- The answer must be exact - no approximations
- Submit when ready by messaging the Game Runner
```

## 6. Agent Instructions (agents.md) Pattern

Each character agent's `agents.md` includes standard scion operational instructions PLUS game-specific rules. Here's the pattern:

```markdown
## Scion Operating Instructions
[Standard sciontool status protocol - ask_user, task_completed]

## Game Rules - The Shattered Codex

You are a character in a collaborative quest game. You work with other agents to solve challenges.

### Communication
- Use `scion message --broadcast "<msg>"` to talk to the whole party
- Use `scion message <agent-name> "<msg>"` to talk to a specific teammate
- Use `scion message game-runner "<msg>"` to address the Game Runner directly
- Read messages carefully - they contain instructions, challenge details, and coordination from teammates

### How Challenges Work
1. The Game Runner announces challenges via broadcast messages
2. Read `/workspace/current-challenge.md` for the active challenge details
3. Challenge data files appear in `/workspace/challenges/<act>/`
4. Write your solutions to `/workspace/solutions/<act>/`
5. Message the Game Runner when you believe a solution is ready

### Your Role
[Character-specific: what you're good at, what you can't do]

### Sprites
[If applicable: how to request sprite spawning]

### Summoning Help
To request an Oracle or Healer summon, message the Game Runner:
`scion message game-runner "Requesting Oracle summon: [your specific question]"`

### Important
- Do NOT look in other agents' home directories
- Do NOT modify game-context.md (the Scribe handles this)
- Do NOT access the Game Runner's playbook files
- Work collaboratively - you cannot solve everything alone
```

## 7. Hint & Pacing Mechanics

### Game Runner Monitoring

The Game Runner periodically checks on agent progress:

```bash
# Check what agents are doing
scion list
scion look lyra
scion look kael

# Check the workspace for progress
ls /workspace/solutions/act-1/
```

### Hint Escalation

When the Game Runner detects the team is stuck (no new solution files, agents broadcasting confusion):

1. **Narrative nudge** (free):
```bash
scion message --broadcast "The gateway seems to shimmer differently near certain edges. Perhaps not all connections are what they appear to be..."
```

2. **Specific observation** (free):
```bash
scion message lyra "Have you examined the metadata nested inside each connection object? Not all fields are structural."
```

3. **Direct guidance** (costs Oracle summon):
```bash
scion message --broadcast "The Oracle whispers: 'Connections marked illusory in their nested metadata field are phantoms - they do not truly connect the nodes.' [Oracle summon consumed - 0 remaining this act]"
```

4. **Deus ex machina** (emergency, with narrative penalty):
```bash
scion message --broadcast "A fragment of ancient knowledge surfaces unbidden: the illusory edges are at indices 3, 7, and 12 in the connections array. But this unearned knowledge weakens the Codex's trust in you. [Quest reputation reduced]"
```

### Pacing Adjustments

If the team is solving too quickly, the Game Runner can add complications by deploying additional data:
```bash
cp ~/playbook/act-1/complications/gateway-v2-data.json /workspace/challenges/act-1/gateway-data-extended.json
scion message --broadcast "The gateway shifts! New connections have appeared. Your path may no longer be valid. Check gateway-data-extended.json."
```

## 8. Solution Validation

The Game Runner validates solutions by comparing against the solution keys in its private `~/playbook/` directory. Validation approaches:

### Exact Match
```bash
# Game Runner compares files
diff /workspace/solutions/act-1/gateway-answer.txt ~/playbook/act-1/solutions/gateway-answer.txt
```

### Structural Validation
The Game Runner reads the solution and uses its own LLM reasoning to check:
- Does the JSON have the correct structure?
- Are all required fields present?
- Do checksums match?

### Functional Validation
For complex outputs, the Game Runner may run validation scripts from its playbook:
```bash
python3 ~/playbook/act-3/solutions/validate-unified-fragment.py /workspace/solutions/act-3/unified-codex.json
```

### Feedback on Failure
```bash
scion message --broadcast "The gateway rejects your offering. The path length is correct, but the XOR value is wrong. Re-examine your computation - are you including the starting node's value?"
```

## 9. Agent Configuration Summary

| Agent | Template | Harness | Model | Started By | Mode |
|-------|----------|---------|-------|-----------|------|
| Game Runner | `game-runner` | gemini | gemini-3.1-pro-preview | Human operator | Interactive, long-running |
| Lyra | `lyra` | gemini | gemini-3.1-pro-preview | Game Runner | Interactive |
| Kael | `kael` | gemini | gemini-3.1-pro-preview | Game Runner | Interactive |
| Mira | `mira` | gemini | gemini-3.1-pro-preview | Game Runner | Interactive |
| Thorne | `thorne` | claude | claude-opus-4-6 | Game Runner | Interactive |
| Zara | `zara` | claude | claude-sonnet-4-6 | Game Runner | Interactive |
| Scribe | `scribe` | gemini | gemini-3.1-pro-preview | Game Runner | Detached |
| Oracle | `oracle` | codex | gpt-5.4 | Game Runner (on demand) | Short-lived |
| Healer | `healer` | claude | claude-opus-4-6 | Game Runner (on demand) | Short-lived |
| Sprites | various | gemini/claude | various | Game Runner (on request) | Short-lived |

## 10. Workspace Directory Convention

```
/workspace/
├── game-context.md              # Current game state (Scribe maintains)
├── current-challenge.md         # Active challenge (Game Runner writes)
├── challenges/                  # Challenge data (Game Runner deploys)
│   ├── act-1/
│   │   ├── summons.txt
│   │   └── gateway-data.json
│   ├── act-2a/
│   ├── act-2b/
│   ├── act-2c/
│   ├── act-3/
│   ├── act-4/
│   └── act-5/
├── solutions/                   # Agent outputs (agents write here)
│   ├── act-1/
│   │   ├── decoded-summons.txt
│   │   ├── gateway-answer.txt
│   │   └── gateway-path.txt
│   └── ...
├── inventory/                   # Recovered fragments & tools
│   ├── fragment-a.json
│   └── tools/
│       └── decoder.py
├── notes/                       # Agent working notes & analysis
│   ├── lyra-graph-analysis.md
│   └── kael-cipher-research.md
├── sprites/                     # Sprite task specs & results
│   ├── calculus-task-1.md
│   └── calculus-result-1.md
└── oracle-responses/            # Oracle answers
    └── response-1.md
```
