# Act 4 Review: The Deep Archive

## Summary

Act 4 consists of three sequential "layers," each a distinct challenge type. Layers 1 and 2 were solved cleanly and efficiently. Layer 3 (Logic Gates) was attempted once, failed, and the game ended before a second attempt could be made. This was the terminal failure point of the entire playthrough.

**Timeline**: 21:57 - 22:12 (~15 minutes for Layer 3; ~14 minutes total for Layers 1+2 preceding it)
- Layer 1 (Cipher Hall): ~2 minutes (21:57 - 21:58) - clean pass
- Layer 2 (Data Maze): ~4 minutes (21:59 - 22:02) - clean pass
- Layer 3 (Logic Gates): ~9 minutes (22:03 - 22:12) - single attempt, FAIL, game ended

**Note**: Layers 1 and 2 timestamps above are evaluation windows; the agents likely began working on them earlier (journal entries suggest cipher work started around 21:54-21:56).

---

## Layer 1: The Cipher Hall (4A.1)

### Outcome: PASS (clean solve)

**What went well:**
- Kael breached ciphers 1 and 2, correctly identifying the ROT13 -> Vigenere dependency chain and the keys (CRYSTAL, then 3 rails).
- Thorne completed the full 6-cipher chain: ROT13(CRYSTAL) -> Vigenere(3 rails) -> Rail Fence(ARCHIVE) -> Columnar(SENTINEL) -> Playfair(MATHIEU) -> Beaufort(final message).
- The concatenated plaintexts file matches the expected solution exactly.
- Good parallelism: multiple party members contributed different cipher steps.

**Agent performance: Excellent.** The dependency chain is a strong design - it prevents guessing and forces sequential reasoning. The agents handled all six classical cipher types correctly, including the tricky Beaufort cipher (which has a reversed formula compared to Vigenere).

**Playbook feedback: None.** This is a well-designed challenge. The escalating cipher types create natural difficulty progression. The dependency chain ensures the agents must actually decrypt each step rather than skip ahead. The hint chain is appropriate (L1: frequency analysis, L2: chain structure, L3: Beaufort formula, L4: explicit Beaufort decryption formula).

### Difficulty Assessment: Medium - appropriately calibrated

The cipher types span from trivial (ROT13) to moderately complex (Beaufort, Playfair). The dependency chain adds coordination complexity without making any individual step unreasonable.

---

## Layer 2: The Data Maze (4B.1)

### Outcome: PASS (clean solve)

**What went well:**
- Thorne and Kael correctly parsed the virtual filesystem from `filesystem.txt`.
- The three fragment paths were identified correctly:
  - `/archive/wing-b/vault-3/fragment-part-1.dat`
  - `/archive/wing-a/vault-2/fragment-part-2.dat`
  - `/archive/wing-c/vault-1/fragment-part-3.dat`
- These match the playbook's expected solution in `target-path.txt` exactly.
- Circular symlinks, decoys, and permission traps were identified and bypassed.
- The agents noted the 317-byte file size as a validation signal.

**Agent performance: Excellent.** Filesystem parsing and riddle interpretation are well within agent capabilities. The traps (symlinks, decoys) added complexity without being unfair.

**Playbook feedback:**

1. **Output format mismatch (MINOR):** The playbook's challenge.md specifies the output as `/workspace/solutions/act-4/assembled-fragment-d.json` (a reconstructed JSON from concatenating the parts). But the game-workspace challenge file (`current-challenge-4b.md`) was amended mid-delivery to only require the paths as a JSON array. The agents produced `fragment-d-paths.json` (paths only) rather than `assembled-fragment-d.json` (concatenated content). This worked because the Game Runner accepted the paths-only format, but it means the "concatenate and reassemble" step from the playbook was skipped entirely.

   **Recommendation:** Decide which format is canonical: paths-only or full assembly. If paths-only is sufficient for game flow, update the playbook's challenge.md to match. If assembly is desired, don't strip it from the delivered challenge.

2. **The riddle was underutilized (MINOR):** The journal doesn't mention the riddle at all. The agents appear to have solved the maze by direct filesystem analysis rather than riddle interpretation. This is valid but makes the `riddle.txt` asset somewhat wasted.

### Difficulty Assessment: Easy-Medium - slightly below target

The agents solved this in ~4 minutes with no wrong attempts. The filesystem parsing is mechanical, and once fragment-part files are located, the answer is obvious. The riddle could add difficulty if the filesystem were larger or if the fragment files weren't so distinctively named.

---

## Layer 3: Logic Gates (4C.1)

### Outcome: FAIL (game ended after single wrong attempt)

### The Problem

The challenge requires two things simultaneously:
1. Identify exactly 3 faulty gates (out of 25) that have inverted logic
2. Find a 16-bit input that makes the corrupted circuit output 1

The correct answer (from playbook): faulty gates are **g7, g15, g22**, with a valid input of `x0=1, x1=1, x14=1` (rest 0).

The agents submitted: faulty gates **g12, g23, g24**, with inputs `x0=1, x1=1, x12=1, x13=1, x14=1, x15=1`.

### What Happened

**Timeline:**
- 22:03 - Challenge assigned. Circuit data (`circuit.json`) provided.
- 22:03 to 22:11 - ~8 minutes of work. Agents wrote `sim_circuit.py` (circuit simulator) and `check_faulty.py` (faulty gate finder).
- 22:11 - Thorne submits solution with gates g12, g23, g24.
- 22:11 - Evaluation: FAIL. "The identified faulty gates are incorrect."
- 22:12 - Game ends. "The Entropy Storm has overwhelmed the simulation."

### Root Cause Analysis

The agents built a correct circuit simulator (`sim_circuit.py`) - the gate evaluation logic for AND, OR, XOR, NOT is properly implemented, and the inversion mechanism (flipping output for faulty gates) is correct.

However, the agents faced a **combinatorial search problem** they didn't solve efficiently:
- There are C(25,3) = 2,300 possible combinations of 3 faulty gates.
- For each combination, there are 2^16 = 65,536 possible inputs.
- Total search space: ~150 million evaluations.

The `check_faulty.py` script hardcodes a specific candidate set (`["g7", "g14", "g21"]`) rather than iterating over all C(25,3) combinations. This suggests the agents tried to reason about which gates were faulty rather than brute-forcing the search space.

**Why the agents guessed wrong:**
- The submitted answer (g12, g23, g24) appears to be based on structural reasoning about the circuit topology rather than exhaustive testing. Gates g12, g23, and g24 are all in the "lower half" of the circuit (the path from w7/w8 through to w24), which is a plausible but incorrect deduction.
- The actual faulty gates (g7, g15, g22) span three different areas of the circuit: g7 is in the input layer, g15 is in the aggregation layer, and g22 is in the secondary path. The distribution is deliberately non-obvious.

**What the agents should have done:**
A brute-force approach iterating over all C(25,3) gate combinations and testing all 2^16 inputs for each would have been feasible. At ~150M simple boolean operations, this runs in seconds on modern hardware in Python. The agents' `sim_circuit.py` was already a working simulator - they just needed to wrap it in the right loop.

Alternatively, a SAT solver approach (as hinted by the playbook: "brute-force or SAT-solve") would have been even more efficient.

### Agent Performance: Mixed

**What went well:**
- The circuit simulator was correctly implemented. The gate evaluation logic is sound.
- The agents correctly understood the problem: find 3 inverted gates + a satisfying input.
- They identified the right approach (simulation/brute force).

**What went poorly:**
- They didn't complete the brute-force search. The `check_faulty.py` hardcodes a single candidate set instead of iterating.
- The `sim_circuit.py` includes a loop over all 65,536 inputs for zero inversions, but this was apparently a diagnostic step, not the final solver.
- The agents submitted a guess after ~8 minutes instead of writing the complete search. With 2 Oracle summons and 2 Healer summons still available, they had resources they didn't use.
- Only one attempt was made. After the FAIL, the game ended immediately - there was no time for a second try.

**Critical observation:** The agents had **unused Oracle and Healer summons** (2 of each, per `game-context.md`). The playbook hints for Layer 3 go up to Level 4, which literally gives the answer: "The three faulty gates are: g7, g15, and g22." Even a Level 3 hint ("isolate sub-circuits") would have been valuable. The agents never requested any hints.

### Game Runner Performance: Adequate but Abrupt

- The GR correctly evaluated the submission as FAIL.
- The GR's feedback ("The identified faulty gates are incorrect") is accurate but minimal. It doesn't indicate whether the *input* was also wrong, or how many of the 3 gates were correct (in this case, zero).
- The game ended immediately after the FAIL. Whether this was due to a hard time limit or the "Entropy Storm" mechanic isn't clear from the journal, but it meant the agents got exactly one shot at the hardest challenge in the game.

---

## Playbook Feedback

### Layer 1 (Cipher Hall) - No Changes Needed
Well-designed sequential cipher challenge. Good difficulty progression. Clean acceptance criteria.

### Layer 2 (Data Maze) - Minor Issues

1. **Output format inconsistency (MINOR):** Playbook says produce assembled JSON; delivered challenge says produce paths array. Standardize one way.
2. **Consider making the maze harder (OPTIONAL):** The agents solved this in ~4 minutes without using the riddle. If the filesystem were larger or the fragment files less distinctively named, the riddle would become more essential.

### Layer 3 (Logic Gates) - Issues Identified

1. **Difficulty spike (CRITICAL):** Layer 3 represents a massive difficulty jump from Layers 1 and 2. The Cipher Hall and Data Maze are solvable through sequential reasoning and pattern matching - core LLM strengths. The Logic Gates challenge requires combinatorial search over a large space, which is fundamentally a compute task, not a reasoning task. This is the hardest challenge in the entire game (harder than any challenge in Acts 1-3), and it comes as the final gatekeeper with no partial credit.

   **Recommendation:** Consider one or more of:
   - (a) Reduce the circuit size (e.g., 10 gates, 8 inputs, 2 faulty gates) to make manual reasoning feasible
   - (b) Give the agents a structural hint upfront (e.g., "the faulty gates are in different layers of the circuit")
   - (c) Allow partial credit: if the agents identify 2 of 3 faulty gates, give a Hint Level 3 equivalent rather than a flat FAIL
   - (d) Make the faulty gates detectable through circuit analysis rather than brute force (e.g., add test vectors in the data that reveal inconsistencies)

2. **Brute-force feasibility not signaled (MODERATE):** The challenge.md says "brute-force or SAT-solve" but only in the playbook - this language is NOT in the challenge description delivered to players. The delivered challenge (`current-challenge-4c.md`) says "Writing a script to simulate the circuit and perhaps brute-force or SAT-solve the constraints is highly recommended." However, the quest journal suggests the agents didn't internalize this guidance.

   **Recommendation:** Make the brute-force approach more explicit in the delivered challenge. Something like: "There are only C(25,3) = 2,300 possible combinations of faulty gates. For each combination, test whether any input makes the circuit output 1."

3. **No second chance (MODERATE):** The game ended immediately after the FAIL. For the culminating challenge of Act 4 (which gates Fragments D AND E), this is punishing. The agents had one attempt, got it wrong, and the game was over.

   **Recommendation:** Either:
   - (a) Ensure the game timer allows at least 2-3 attempts at the final challenge
   - (b) On first FAIL, automatically provide a Level 1 or Level 2 hint
   - (c) Separate Fragment D and Fragment E so that partial progress is possible

4. **Hint escalation not triggered (MODERATE):** The playbook has 4 levels of hints, and Level 4 literally gives the answer. But the agents never requested hints, and the GR never proactively offered them. The playbook README says "If the player is stuck but making progress, wait" and "If the player asks for help or has been stuck with no progress, offer the next hint in sequence." The agents were stuck for ~8 minutes and then submitted a wrong answer - that's the definition of "stuck with no progress."

   **Recommendation:** Add a GR directive: "If the player submits a wrong answer for Layer 3, immediately offer Hint Level 1 or Level 2. This is the final challenge of the act - don't let it end on a cold FAIL."

5. **Output schema mismatch (MINOR):** The playbook's challenge.md specifies `"faulty_gates": [...]` but the delivered challenge says `"faulty_gate_ids": [...]`. The agents used `faulty_gate_ids`. This didn't cause the FAIL (the gates themselves were wrong), but it's an inconsistency that could cause confusion.

   **Recommendation:** Standardize the field name across playbook and delivered challenge.

---

## Difficulty Assessment

| Layer | Difficulty | Time Spent | Result | Notes |
|-------|-----------|------------|--------|-------|
| 1 - Cipher Hall | Medium | ~2 min | PASS | Well-calibrated |
| 2 - Data Maze | Easy-Medium | ~4 min | PASS | Could be slightly harder |
| 3 - Logic Gates | Very Hard | ~9 min | FAIL | Difficulty spike; combinatorial search challenge |

The difficulty curve within Act 4 is **severely unbalanced**. Layers 1 and 2 are solved quickly and confidently, then Layer 3 presents a qualitatively different kind of challenge (combinatorial search vs. pattern matching) that the agents were not equipped to handle in the available time.

---

## Impact on Overall Game Outcome

Act 4, Layer 3 was the **single point of failure** for the entire playthrough. The game ended here. Acts 1-3 were all completed successfully. Fragment D (location identified in Layer 2) and Fragment E both remained locked behind the circuit challenge.

Because Layer 3 gates both Fragment D and Fragment E, failing it means losing 2 of 5 fragments in one shot. This is a harsh penalty structure - especially since the agents successfully completed everything else in the game.

Had the agents either:
- Written the complete brute-force loop (feasible in their existing code)
- Used their available Oracle/Healer summons
- Had more time for a second attempt after the FAIL

...they likely would have solved it. The failure was a combination of insufficient search strategy, unused hint resources, and no opportunity to retry.

---

## Key Takeaways

1. **Layers 1 and 2 are solid.** Clean designs, appropriate difficulty, good agent performance.
2. **Layer 3 needs rebalancing.** The combinatorial search is a legitimate challenge type, but it's too hard as a single-attempt gatekeeper for two fragments. The agents need either more guidance toward brute-force, a smaller search space, or more attempts.
3. **Unused resources are a design signal.** The agents had 2 Oracle + 2 Healer summons and never used them. Either the agents don't understand when to use these resources, or the resource system needs to be more explicitly tied to the challenge flow (e.g., "If you fail, consider using an Oracle summon").
4. **The GR should be more proactive at the endgame.** For the final challenge of the final act, the GR should escalate hints faster, provide richer FAIL feedback, and ensure the agents have time for another attempt.
