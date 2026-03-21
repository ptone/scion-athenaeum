# Quest Scenario: The Shattered Codex

## Backstory

The Codex Machina was an ancient computational artifact - a self-documenting system that contained the complete operational knowledge of the Archive Kingdoms. When the Codex was shattered by the Entropy Storm, its five fragments scattered across the realms, each fragment encoding its knowledge in the native format of the land where it fell. The fragments are degrading. If not recovered and reassembled, the knowledge is lost forever.

## Quest Graph

```
                    [Act I: The Gathering]
                           |
                    Decode the Summons
                           |
                    Assemble the Party
                           |
                    Solve the Gateway Cipher
                           |
              ____________|____________
             |            |            |
        [Act II-A]   [Act II-B]   [Act II-C]
        Realm of     Realm of     Realm of
        Formats      APIs         Patterns
        (Mira+Lyra)  (Kael+Zara)  (Thorne+Lyra)
             |            |            |
             |____________|____________|
                          |
                   [Act III: The Convergence]
                          |
                   Unify the Fragments
                          |
                   [Act IV: The Deep Archive]
                          |
                   Layer 1: The Cipher Hall
                          |
                   Layer 2: The Data Maze
                          |
                   Layer 3: The Logic Gates
                          |
                   [Act V: The Restoration]
                          |
                   Assemble & Activate
```

---

## Act I: The Gathering (Serial - All Characters)

### Challenge 1.1: Decode the Summons
**Revealed at start. All characters present.**

The Game Runner places a file `summons.txt` in the workspace. It contains a message encoded with a multi-layer encoding:
- Base64 outer layer
- ROT13 middle layer
- A substitution cipher inner layer, with the key hidden in the file's metadata (a comment line that looks like noise)

**What it takes:**
- Lyra writes a decoder script
- Kael researches the cipher pattern (it's based on a real historical cipher)
- Thorne validates the decoded message makes sense
- The decoded message reveals the quest objective and a hint about where to find the Gateway

**Difficulty lever:** The substitution cipher key isn't immediately obvious. The "noise" comment contains coordinate pairs that map to a letter substitution table. This requires Mira to parse the structure and Lyra to implement the mapping.

**Success criteria:** The team produces a correctly decoded plaintext message.

---

### Challenge 1.2: Solve the Gateway Cipher
**Revealed after 1.1 completes.**

The decoded summons references a "Gateway" that can only be opened by computing a specific value. The Game Runner places a `gateway-data.json` file containing:
- A large nested JSON structure (~500 lines) representing a "map" of interconnected nodes
- Each node has a name, value, and connections to other nodes
- The team must find the shortest path between two specific nodes and compute the XOR of all node values along that path

**What it takes:**
- Mira parses and flattens the complex JSON structure into a workable graph representation
- Lyra implements a shortest-path algorithm (BFS/Dijkstra)
- Thorne writes tests to verify the path is actually shortest and the XOR is correct
- Zara integrates the components into a runnable solution
- Kael may need to research specific graph algorithm details if the structure has unusual properties

**Difficulty lever:** The JSON structure contains deliberate red herrings - some connections are marked "illusory" in a nested metadata field that's easy to overlook. Including these false edges leads to a wrong answer.

**Success criteria:** The team produces the correct XOR value, which the Game Runner validates.

---

## Act II: The Fracture (Parallel - Party Splits)

After solving the Gateway, the Game Runner reveals that three Codex fragments are in three separate realms. The party must decide how to split up. The Game Runner provides brief descriptions of each realm but NOT the specific challenges within.

**Party allocation is a strategic decision.** The Game Runner describes the realms only as:
- "A realm where knowledge is trapped in incompatible forms"
- "A realm where knowledge must be retrieved from distant sources"
- "A realm where knowledge is hidden behind logical barriers"

The team must decide who goes where based on these vague descriptions. Sub-optimal allocation makes the challenges harder but not impossible.

### Act II-A: Realm of Formats (Suggested: Mira + one other)

#### Challenge 2A.1: The Format Gauntlet
The Codex fragment here has been split into 5 files, each in a different format:
- A CSV with inconsistent delimiters and encoding issues
- An XML file with a non-standard namespace scheme
- A YAML file with anchors and aliases that create circular references
- A fixed-width text file with no header documentation
- A binary-encoded file (actually base64 of a msgpack structure)

The team must convert ALL of them into a single unified JSON structure. The fragment's meaning only becomes clear when all 5 are correctly merged.

**What it takes:**
- Mira's data transformation skills are critical
- Flux Motes can handle individual conversions in parallel
- But someone needs to figure out the unified schema (what fields map to what)
- Lyra or Zara can help with the trickier parsing (msgpack, circular YAML)

**Difficulty lever:** The fixed-width file's column positions can only be determined by cross-referencing patterns in the CSV. The field names don't match across formats - semantic understanding is needed.

#### Challenge 2A.2: The Integrity Check
Once merged, the unified JSON contains checksums that must be validated. Three of the records have been "corrupted" and must be identified and repaired using redundancy data embedded in other records.

**What it takes:**
- Thorne-type validation skills (or a remote Thorne consultation via shared files)
- Lyra-type logic to compute and compare checksums
- May require summoning the Healer if corruption is too deep

**Success criteria:** A clean, validated JSON fragment file.

---

### Act II-B: Realm of APIs (Suggested: Kael + one other)

#### Challenge 2B.1: The Information Hunt
The Codex fragment in this realm is encoded as a series of clues. Each clue references a real-world fact that must be researched:
- "The atomic number of the element discovered in the year the Eiffel Tower was completed"
- "The population rank among world cities of the birthplace of the inventor of the World Wide Web"
- "The number of bones in the appendicular skeleton of a domestic cat"

There are 8-10 such clues. Each answer becomes a number. The numbers form coordinates into a large data file (`archive-index.dat`) that the Game Runner provides.

**What it takes:**
- Kael's research ability is essential - Seeker Wisps can research clues in parallel
- Answers must be precise (exact numbers, not approximations)
- Zara or another character extracts data at the computed coordinates
- Some clues are deliberately tricky or have multiple plausible answers

**Difficulty lever:** 2-3 of the clues have ambiguous answers depending on the source. The team may need to try multiple interpretations, or summon the Oracle for a definitive answer.

#### Challenge 2B.2: The API Labyrinth
The extracted data from the archive-index reveals a URL pattern for a mock API (simulated via local files by the Game Runner). The team must:
- Discover the API's structure by examining response patterns
- Navigate a paginated, linked-data structure to find the fragment
- Handle rate limiting (simulated) and authentication tokens (embedded in earlier data)

**What it takes:**
- Kael understands API patterns and can map the structure
- Zara or Lyra writes the traversal code
- The authentication token was hidden in the Act I gateway data (requires going back to look)

**Success criteria:** Successfully retrieve the complete Codex fragment data from the API.

---

### Act II-C: Realm of Patterns (Suggested: Lyra/Thorne + one other)

#### Challenge 2C.1: The Logic Grid
A logic puzzle expressed as a constraint satisfaction problem. The Game Runner provides:
- A grid (8x8) with some cells pre-filled
- A set of 12-15 constraint rules (like Sudoku but with custom rules)
- Rules reference row/column relationships, neighbor conditions, and aggregate functions

The team must write a solver that fills the grid correctly.

**What it takes:**
- Lyra's algorithm skills to implement a constraint solver (backtracking with constraint propagation)
- Thorne to validate that each constraint is correctly implemented and the solution satisfies all rules
- Calculus Sprites can try different solving strategies in parallel

**Difficulty lever:** Some constraints are expressed in natural language that's deliberately ambiguous. "No two adjacent cells share a factor" - does diagonal count as adjacent? The Game Runner won't clarify unless an Oracle is summoned.

#### Challenge 2C.2: The Pattern Lock
The solved grid's values encode a transformation that must be applied to a data file to extract the fragment. The transformation is a sequence of operations:
- Row values define byte offsets
- Column values define bit masks
- The operation sequence matters (not commutative)

**What it takes:**
- Understanding the encoding scheme (Kael-type research or Oracle consultation)
- Implementing the extraction (Lyra)
- Verifying the output (Thorne)

**Success criteria:** A correctly extracted Codex fragment.

---

## Act III: The Convergence (Serial - Full Party)

### Challenge 3.1: Fragment Unification
**All three sub-teams return with their fragments.**

The three fragments are in different formats and reference systems:
- Fragment A: JSON with nested arrays, using 1-based indexing
- Fragment B: Key-value pairs with namespaced keys, using UUID references
- Fragment C: A custom binary-like format (hex-encoded structured data)

They must be unified into a single coherent document. But they don't simply concatenate - they interleave. Each fragment contains "anchor points" that reference locations in the other fragments.

**What it takes:**
- Mira transforms each fragment into a common intermediate format
- Lyra resolves the cross-references and anchor points programmatically
- Kael identifies the semantic meaning of the anchor points (they follow a pattern from a real data standard)
- Thorne validates that the cross-references are correctly resolved
- Zara orchestrates the merge and produces the unified output
- Every character contributes something essential

**Difficulty lever:** The anchor point resolution has an ordering dependency. Resolving fragment A's anchors requires data from B, B's from C, and C's from A (circular dependency). The team must find a fixpoint or iterative resolution strategy.

**Success criteria:** A single unified document that passes the Game Runner's integrity check.

---

## Act IV: The Deep Archive (Serial - Full Party)

The unified fragments reveal coordinates to the Deep Archive, where the final two Codex pieces reside. The archive is a layered structure - each layer must be solved to access the next.

### Challenge 4.1: Layer 1 - The Cipher Hall
A collection of 6 files, each encrypted with a different classical cipher:
- Caesar, Vigenere, Rail Fence, Columnar Transposition, Playfair, and one unknown
- The key for each cipher is derived from the content of another decrypted file (dependency chain)
- But one file can be decrypted without a key (it's a simple frequency analysis target)

**What it takes:**
- Lyra implements cipher-specific decoders
- Kael identifies the unknown cipher through research
- The dependency chain means some work is serial, but multiple starting points exist
- Thorne validates each decryption by checking for coherent plaintext

**Difficulty lever:** The Playfair cipher uses a non-standard variant. The unknown cipher is a real but obscure historical cipher that requires specific research to identify.

### Challenge 4.2: Layer 2 - The Data Maze
The decrypted files describe a virtual filesystem - directories, files, and symbolic links defined in a structured text format. The team must:
- Parse the filesystem description and build it as actual directories/files
- Navigate to a specific file, but the path is described as a riddle
- Handle circular symlinks and permission flags that gate access
- The target file is split across 3 locations with parts that must be assembled in order

**What it takes:**
- Mira builds the filesystem from the description
- Lyra handles symlink resolution and circular reference detection
- Kael interprets the riddle to determine the target path
- Zara assembles the file parts

**Difficulty lever:** The filesystem is large (~200 entries). Some paths lead to decoy files. The permission flags encode a puzzle of their own.

### Challenge 4.3: Layer 3 - The Logic Gates
The assembled file contains a description of a Boolean circuit - a network of AND, OR, NOT, and XOR gates with ~30 inputs and a single output. The team must:
- Parse the circuit description
- Determine the input combination that produces output=1
- But: 5 of the gates are "faulty" (their truth tables are inverted)
- The faulty gates aren't labeled - they must be identified through testing

**What it takes:**
- Lyra builds a circuit simulator
- Thorne systematically tests gate behaviors to identify faulty ones
- Ward Echoes can test different gate combinations in parallel
- Once faults are identified, Lyra solves for the correct input

**Difficulty lever:** With 30 inputs, brute force over all 2^30 combinations is infeasible in reasonable time. The team needs a smarter approach - perhaps SAT solving, or identifying faults first to reduce the search space. This is the hardest single challenge in the quest.

**Success criteria for Act IV:** The correct input combination unlocks the fourth Codex fragment, and the circuit's internal state at the solution reveals the fifth.

---

## Act V: The Restoration (Collaborative Finale)

### Challenge 5.1: Assembly Protocol
All five fragments must be assembled into the complete Codex. But the assembly is a protocol, not just concatenation:

1. Fragments must be sorted by their embedded sequence numbers
2. Overlapping sections between adjacent fragments must be resolved (conflict resolution)
3. A checksum computed across all fragments must match an expected value
4. The final document must be rendered in a specific output format

Each step requires a different character's expertise, and they must execute in coordination:
- Mira: format normalization and overlap detection
- Lyra: sequence number extraction and checksum computation
- Kael: research the expected output format (it follows a real specification)
- Thorne: validate each assembly step before proceeding
- Zara: orchestrate the pipeline and produce the final output

**Success criteria:** The Game Runner validates the assembled Codex. If correct, the quest is complete.

---

## Resource Constraints (Per Chapter)

| Resource | Act I | Act II (per sub-team) | Act III | Act IV | Act V |
|----------|-------|-----------------------|---------|--------|-------|
| Oracle Summons | 1 | 1 | 1 | 2 | 0 |
| Healer Summons | 1 | 1 | 2 | 2 | 1 |
| Max Sprites Active | 3 | 2 | 4 | 4 | 5 |

## Game Runner Evaluation Criteria

For each challenge, the Game Runner evaluates:
1. **Correctness** - Does the output match expected results?
2. **Completeness** - Are all parts of the challenge addressed?
3. **Process** - Did the team collaborate effectively (use multiple characters)?

The Game Runner does NOT evaluate:
- Code quality or style
- Speed of completion
- Elegance of solution

## Failure Modes

- **Wrong answer:** Game Runner provides a hint (costs an Oracle summon) and the team can retry
- **Stuck:** After extended struggle, Game Runner can provide a nudge (narrative hint, not solution)
- **Critical failure:** If a fragment is irrecoverably corrupted (team made destructive changes), the Healer can attempt restoration but with incomplete results, making later challenges harder
- **Resource exhaustion:** If Oracle/Healer summons are used up, the team must proceed without safety nets
