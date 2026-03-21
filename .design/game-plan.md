# Relics of the Athenaeum: Game Plan

## Overview

"Relics of the Athenaeum" is a multi-agent collaborative quest where 5 main characters, 2-3 peripheral characters, and various summoned entities work together to recover fragments of an ancient computational artifact - the Codex Machina - that has been scattered across five distinct realms. Each realm presents challenges that require genuine coding, research, data transformation, and collaborative problem-solving.

The game is orchestrated by a Game Runner (Dungeon Master) agent that controls pacing, reveals challenges, evaluates solutions, and manages the shared game state.

## Design Principles

1. **Genuine challenge** - Problems should require real computation, research, and creative problem-solving. No pre-baked answers.
2. **Collaboration required** - No single character can solve everything alone. Skills must be combined.
3. **Discovery over prescription** - Characters don't know all challenges upfront; the Game Runner reveals them progressively.
4. **Branching paths** - Some challenges can be tackled in parallel by splitting the party.
5. **Failure is possible** - Challenges have real constraints (time, correctness, resource limits) that can result in failure or partial success.
6. **Emergent strategy** - The team must decide how to allocate their skills and resources.

## Document Index

- [quest-premise.md](quest-premise.md) - Original premise
- [characters.md](characters.md) - All character definitions, skills, and abilities
- [quest-scenario.md](quest-scenario.md) - The full quest scenario, realms, and challenge graph
- [game-mechanics.md](game-mechanics.md) - Rules, state management, and game runner logic
- [scion-templates.md](scion-templates.md) - Scion template specifications for all agents

## High-Level Quest Arc

### Act I: The Gathering (Serial)
The Game Runner sets the scene. Characters are introduced and given the initial quest hook. They must decode an initial puzzle together to learn where the Codex fragments are scattered.

### Act II: The Fracture (Parallel branches converging)
The party learns that three Codex fragments are in three different realms. They must split into sub-teams to recover fragments simultaneously (parallel work). Each sub-team faces realm-specific challenges.

### Act III: The Convergence (Serial with collaboration)
Sub-teams return. The recovered fragments must be combined, but they're encoded in incompatible formats. A unification challenge requires all characters to contribute their specializations.

### Act IV: The Deep Archive (Serial)
The unified fragments reveal the location of the final two pieces, deep in a layered archive. The full party must navigate a sequence of escalating challenges together.

### Act V: The Restoration (Collaborative finale)
The complete Codex must be assembled and activated. This requires a final multi-step challenge where different characters must execute coordinated tasks in the right order.

## Character Roster Summary

| Role | Type | Core Capability | Key Skill |
|------|------|-----------------|-----------|
| Lyra the Logician | Main | Code & algorithms | Writes code to solve computational problems |
| Kael the Chronicler | Main | Research & synthesis | Web research, information gathering |
| Mira the Mapper | Main | Data transformation | File manipulation, format conversion |
| Thorne the Sentinel | Main | Validation & testing | Writes tests, verifies correctness |
| Zara the Weaver | Main | Integration & orchestration | Combines outputs, builds pipelines |
| The Oracle | Peripheral | Deep knowledge queries | Answers specific domain questions (summoned) |
| The Healer | Peripheral | Error recovery | Debugs, fixes broken code/data (summoned) |
| The Scribe | Peripheral | Documentation | Records progress, maintains shared state |

See [characters.md](characters.md) for full details.
