# Playbook Build Plan

## Status Overview

The game runner's playbook lives at `.scion/templates/game-runner/home/playbook/`.
This `home/` directory is mounted as the game runner agent's home directory (`~/`),
so it accesses files as `~/playbook/act-1/challenge-1.1/data/summons.txt` etc.

| Act | Data Files | Solution Files | challenge.md | Status |
|-----|-----------|---------------|-------------|--------|
| Act 1 (1.1 + 1.2) | Done | Done | Done | **COMPLETE** |
| Act 2 Realm of Formats (2A.1 + 2A.2) | Done | Done | Done | **COMPLETE** |
| Act 2 Realm of APIs (2B.1 + 2B.2) | Done | Done | Done | **COMPLETE** |
| Act 2 Realm of Patterns (2C.1 + 2C.2) | Done | Done | Done | **COMPLETE** |
| Act 3 (3.1) | Done | Done | Done | **COMPLETE** |
| Act 4 Layer 1 - Cipher Hall | Done | Done | **MISSING** | Needs challenge.md + dependency-chain.md |
| Act 4 Layer 2 - Data Maze | Done | Done | **MISSING** | Needs challenge.md |
| Act 4 Layer 3 - Logic Gates | Done | Done | **MISSING** | Needs challenge.md |
| Act 5 Assembly Protocol | N/A | Done | **MISSING** | Needs challenge.md |

Also needed: **agents.md path reconciliation** (see bottom of this doc).

---

## Fragment Schema (shared across acts)

All 5 fragments follow a common schema. The exact content is already baked into the
solution files. Here are the fragment IDs and their anchor-point cross-references
(critical for Act 3 unification):

| Fragment | Seq | Origin | Anchors To |
|----------|-----|--------|-----------|
| A | 1 | Realm of Formats | ref_B_1: ANCHOR-B-7f3a9d, ref_C_1: ANCHOR-C-2d1e8b |
| B | 2 | Realm of APIs | ref_C_1: ANCHOR-C-9b4c2e, ref_A_1: ANCHOR-A-5e8d1f |
| C | 3 | Realm of Patterns | ref_A_1: ANCHOR-A-3f7b4c, ref_B_1: ANCHOR-B-1a6e5d |
| D | 4 | The Deep Archive | (none) |
| E | 5 | The Deep Archive | (none) |

Anchor resolution (for Act 3 + Act 5 cross_references):
- ANCHOR-A-5e8d1f → Fragment A, record R001
- ANCHOR-A-3f7b4c → Fragment A, record R003
- ANCHOR-B-7f3a9d → Fragment B, record G001
- ANCHOR-B-1a6e5d → Fragment B, record G003
- ANCHOR-C-2d1e8b → Fragment C, record T001
- ANCHOR-C-9b4c2e → Fragment C, record T003

---

## Task 1: Act 3 challenge.md

**File:** `act-3/challenge-3.1/challenge.md`

**What it needs:**
- Narrative: Three sub-teams return, fragments speak different languages, circular anchor dependencies
- Setup: Copy fragment-a-recovered.json, fragment-b-recovered.json, fragment-c-recovered.json to /workspace/challenges/act-3/
- Explain the 3 input formats:
  - Fragment A: 1-based nested arrays (see data/fragment-a-recovered.json)
  - Fragment B: Flat namespaced key-value pairs like `codex.atlas.G001.region`
  - Fragment C: Hex-encoded JSON records
- Objective: Unify into a single JSON with cross-references resolved
- Output: /workspace/solutions/act-3/unified-codex-partial.json
- Solution key: compare against solutions/unified-codex-partial.json (already exists)
- Validation: run solutions/validate-unification.py (already exists)
- Hints:
  1. "Each fragment encodes the same kind of knowledge - records with IDs - but the shapes differ"
  2. "Fragment C's hex strings are UTF-8 encoded JSON objects"
  3. "The anchor points create circular dependencies - A references B, B references C, C references A. Resolve them iteratively"
  4. (Oracle-cost) "Parse all three into a common record format first, then resolve anchors by matching ANCHOR-X-* IDs to record IDs within each fragment"
- Acceptance: validate-unification.py returns PASS

---

## Task 2: Act 4 Layer 1 challenge.md + dependency-chain.md

**Files:**
- `act-4/layer-1-cipher-hall/challenge.md`
- `act-4/layer-1-cipher-hall/solutions/dependency-chain.md`

**What it needs:**
- Narrative: Six sealed chambers, each with a different cipher
- Setup: Copy cipher-1.txt through cipher-6.txt to /workspace/challenges/act-4/cipher-hall/
- Explain the dependency chain (this is also the dependency-chain.md content):
  - cipher-1.txt: Caesar/ROT13 (solvable independently via frequency analysis)
  - plain-1 contains the Vigenere key → "CRYSTAL"
  - cipher-2.txt: Vigenere with key CRYSTAL
  - plain-2 contains the rail count → 3
  - cipher-3.txt: Rail Fence with 3 rails
  - plain-3 contains the columnar key → "ARCHIVE"
  - cipher-4.txt: Columnar Transposition with key ARCHIVE
  - plain-4 contains the Playfair keyword → "SENTINEL"
  - cipher-5.txt: Playfair (standard 5x5, I/J combined) with keyword SENTINEL
  - plain-5 contains the Beaufort key → "MATHIEU"
  - cipher-6.txt: Beaufort cipher with key MATHIEU (the "unknown" cipher)
  - plain-6 reveals Fragment D's location
- Solution key: plain-1.txt through plain-6.txt (already exist)
- Hints:
  1. "The first chamber's cipher is one of the simplest known - try counting letter frequencies"
  2. "Each solved cipher reveals the key for the next. Start with cipher-1"
  3. "The sixth cipher resembles Vigenere but the encryption formula is reversed: C = (K - P) mod 26"
  4. (Oracle-cost) "The unknown cipher is a Beaufort cipher. Decryption: P = (K - C) mod 26"
- Acceptance: All 6 plaintexts match solution files

**Data quality note:** Verify cipher-2 through cipher-6 are correctly encrypted. cipher-1 is confirmed ROT13. Spot-check at least cipher-2 (Vigenere with key CRYSTAL) by decrypting the first few characters.

---

## Task 3: Act 4 Layer 2 challenge.md

**File:** `act-4/layer-2-data-maze/challenge.md`

**What it needs:**
- Narrative: A virtual filesystem materializes from the decrypted cipher texts
- Setup: Copy filesystem.txt and riddle.txt to /workspace/challenges/act-4/data-maze/
- Explain the filesystem format (DIR, FILE, SYMLINK entries in filesystem.txt)
- Objective: Parse the filesystem, solve the riddle, find 3 file parts, assemble Fragment D
- Output: /workspace/solutions/act-4/assembled-fragment-d.json
- Solution key: solutions/target-path.txt (3 paths) and solutions/assembled-file.txt (Fragment D JSON)
- Hints:
  1. "Beware of circular symlinks - detect and skip them"
  2. "The riddle mentions 'three parts in three vaults' - look for fragment-part-*.dat files"
  3. "The parts must be read in numerical order and concatenated"
  4. (Oracle-cost) Reveal the 3 exact file paths
- Acceptance: assembled file matches Fragment D JSON

**Data quality note:** Review filesystem.txt to ensure the 3 target files actually exist as entries, the riddle is solvable, and circular symlinks are present but avoidable.

---

## Task 4: Act 4 Layer 3 challenge.md

**File:** `act-4/layer-3-logic-gates/challenge.md`

**What it needs:**
- Narrative: The deepest chamber contains a Boolean circuit, the Archive's final lock
- Setup: Copy circuit.json to /workspace/challenges/act-4/logic-gates/
- Explain: 16 inputs, 25 gates (AND/OR/NOT/XOR), 1 output. 3 gates are faulty (inverted output). Must find input that produces output=1 WITH the faults.
- The faulty gates are NOT labeled - teams must identify them by testing
- Objective: Find the correct 16-bit input AND identify the 3 faulty gates
- Output: /workspace/solutions/act-4/circuit-solution.json with input bits and faulty gate IDs
- Solution key: solutions/correct-input.json and solutions/faulty-gates.json
- After solving, Fragments D and E are "revealed" (Game Runner copies them to workspace)
- Hints:
  1. "Test individual gates by tracing simple inputs through the circuit"
  2. "A faulty gate produces the opposite of its expected truth table output"
  3. "Try isolating sections of the circuit - test sub-circuits independently"
  4. (Oracle-cost) Reveal the 3 faulty gate IDs
- Acceptance: correct input combination AND correct faulty gate identification

**Data quality note:** Verify the circuit is actually solvable. Run the circuit simulator with the solution input and faulty gates to confirm output=1. Check solutions/correct-input.json and solutions/faulty-gates.json are consistent with circuit.json.

---

## Task 5: Act 5 challenge.md

**File:** `act-5/assembly-protocol/challenge.md`

**What it needs:**
- Narrative: Epic finale - all 5 fragments recovered, the final assembly protocol
- Setup: All 5 fragments should be in /workspace/inventory/ by this point
- Assembly protocol steps:
  1. Sort fragments by sequence_number (1-5)
  2. Resolve cross-references using the anchor point mapping
  3. Compute integrity SHA-256 hash of all fragment content concatenated in order
  4. Produce the final Codex JSON structure (see complete-codex.json)
- Output: /workspace/solutions/act-5/complete-codex.json
- Solution key: solutions/complete-codex.json (already exists)
- Validation: solutions/validate-codex.py (already exists)
- Hints: None (Act V has 0 Oracle summons)
- Acceptance: validate-codex.py returns PASS
- On success: Game Runner delivers epic finale narrative and signals game completion

---

## Task 6: Data Quality Audit

After all challenge.md files are written, do a full audit:

1. **Act 1.1**: Decode summons.txt end-to-end (base64 → ROT13 → substitution → plaintext)
2. **Act 1.2**: Run BFS on gateway-data.json excluding illusory edges, verify path and XOR
3. **Act 2A**: Parse all 5 format files and verify they produce Fragment A records
4. **Act 2B**: Follow API navigation path and verify Fragment B extraction
5. **Act 2C**: Verify logic grid satisfies all constraints; verify hex decode of pattern-data
6. **Act 3**: Verify all 3 recovered fragment formats parse correctly; run validate-unification.py
7. **Act 4.1**: Verify each cipher encrypts/decrypts correctly through the dependency chain
8. **Act 4.2**: Verify filesystem.txt contains the 3 target paths; verify riddle is solvable
9. **Act 4.3**: Simulate circuit with solution input + faulty gates → output must be 1
10. **Act 5**: Run validate-codex.py against complete-codex.json

---

## Task 7: Path Reconciliation

The game runner's `agents.md` references paths that must match the playbook structure.
Currently agents.md line 169 says:

> Copy challenge data files from `~/playbook/act-X/challenge-Y/data/` to `/workspace/challenges/act-X/challenge-Y/`

This works for Act 1 (`act-1/challenge-1.1/data/`) but Act 2 uses a different structure
(`act-2/realm-formats/challenge-2a.1/data/`). The agents.md and system-prompt.md may need
updates to match, OR the challenge.md files should contain explicit copy commands for the
Game Runner to follow. Currently each challenge.md has setup instructions, so this should
be fine as long as the Game Runner reads challenge.md before deploying.

Verify that the Game Runner's initialization protocol (agents.md line 160) matches the
actual Act 1 path structure. Current agents.md says:
```
Copy challenge data from ~/playbook/act-1/challenge-1.1/data/ to /workspace/challenges/act-1/
```
This should work with the current file structure.
