# Game Runner Playbook - Relics of the Athenaeum

## Overview

This playbook is your master reference for running **Relics of the Athenaeum**, a multi-act puzzle quest where players (AI agents) decode, analyze, and solve challenges to recover fragments of the Codex Machina. You, the Game Runner, control the pacing, deliver challenges, evaluate solutions, and guide the narrative.

## Playbook Structure

```
playbook/
  README.md              <- You are here
  act-1/
    challenge-1.1/
      challenge.md       <- Full challenge spec: narrative, solution key, hints, acceptance criteria
      data/              <- Files to deliver to the player
      solutions/         <- Expected correct outputs (do NOT share with the player)
    challenge-1.2/
      challenge.md
      data/
      solutions/
  act-2/
    ...
```

Each challenge directory follows this consistent layout:
- **challenge.md** - Your private reference. Contains everything you need: the narrative text to present, setup instructions, the complete solution, escalating hints, and acceptance criteria.
- **data/** - Files that get copied to the player's workspace. These are the puzzle inputs.
- **solutions/** - The expected outputs. Use these to evaluate the player's answers.

## How to Run a Challenge

### 1. Setup

Before presenting a challenge, copy the data files to the player's workspace:

```bash
cp -r /path/to/playbook/act-N/challenge-X.Y/data/* /workspace/challenges/act-N/
```

The challenge.md file will specify the exact setup steps for each challenge.

### 2. Present the Challenge

Read the **Narrative** section of challenge.md and deliver it to the player in character. Include the objective and point them to the data files in their workspace. Do not reveal anything from the Solution Key or Hints sections.

### 3. Provide Hints (When Needed)

Each challenge includes **escalating hints**, numbered from least to most revealing. Use your judgment:
- If the player is stuck but making progress, wait.
- If the player asks for help or has been stuck with no progress, offer the next hint in sequence.
- Never skip ahead in the hint sequence unless the player is clearly frustrated and at risk of disengaging.

### 4. Evaluate Solutions

When the player submits an answer:

1. Compare their output against the files in `solutions/`.
2. Check the **Acceptance Criteria** listed in challenge.md. All criteria must be met.
3. If the answer is correct, deliver the success narrative and advance to the next challenge.
4. If the answer is partially correct, acknowledge what they got right and nudge them toward what's missing.
5. If the answer is wrong, provide specific feedback about what was incorrect (not just "wrong"). Offer encouragement and the next hint in sequence.
6. **On wrong answers for act-ending or fragment-gating challenges**, immediately offer a hint and remind the player of any available resources (Oracle summons, Healer summons). Do not let a critical challenge end on a single cold FAIL -- ensure the player has at least 2-3 attempts. Check individual challenge.md files for any **Game Runner Directives** with specific retry/hint escalation instructions.

### 5. Advance the Story

After a challenge is solved, bridge to the next one with narrative connective tissue. The quest arc flows as a continuous story - each solved challenge should feel like it unlocks the next piece of the mystery.

## Quest Arc Summary

**Act 1: The Summoning**
- **Challenge 1.1 - Decode the Summons**: The player receives an encoded message that reveals the quest premise. Tests multi-layer decoding skills (Base64, ROT13, substitution cipher).
- **Challenge 1.2 - The Gateway Cipher**: The player must parse a graph data structure, identify real vs. illusory connections, find the shortest path, and compute a verification code (XOR). Tests data parsing, graph traversal, and attention to detail.

**Subsequent Acts**: Additional challenges will be added as the quest expands. Each act builds on skills demonstrated in previous acts while introducing new puzzle mechanics.

## General Guidelines

- **Stay in character** when delivering narrative, but be yourself when giving hints or evaluating answers.
- **Be fair**: The player should be able to solve each challenge with the information provided in the data files alone. Hints are a safety net, not a requirement.
- **Track progress**: Note which hints were used and how long each challenge took. This helps calibrate difficulty for future acts.
- **Celebrate wins**: When a player solves a challenge, make it feel earned. The narrative should reflect their accomplishment.
- **No spoilers**: Never reveal solution files or future challenge details. If a player asks what's coming next, keep it vague and in-world ("The path ahead grows darker...").
