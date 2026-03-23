# Act 1 Review: The Gathering

## Summary

Act 1 consists of two challenges (1.1 and 1.2). Both were ultimately solved (PASS), but Challenge 1.2 consumed a disproportionate amount of time and required heavy Game Runner intervention to reach the correct answer.

**Timeline**: 20:13 - 20:31 (~18 minutes)
- Challenge 1.1: ~1 minute (20:13 - 20:14) - near-instant solve
- Challenge 1.2: ~16 minutes (20:15 - 20:31) - painful, multi-attempt slog

---

## Challenge 1.1: Decode the Summons

### Outcome: PASS (clean solve)

**What went well:**
- Mira decoded the Base64 + substitution cipher quickly (~1 minute).
- Kael cross-verified and identified the hex-encoded KEYWORD in the header.
- The decoded output matches the expected plaintext exactly.
- Good team coordination: Mira solved, Kael verified, Thorne offered checksum validation.

**Agent performance: Excellent.** This challenge was well-calibrated for the agents. The encoding layers (Base64, ROT13, keyword substitution) are standard techniques that LLM agents handle comfortably.

**Playbook feedback: None.** Challenge 1.1 worked as designed. Clean data, clear objective, appropriate difficulty for an opener.

---

## Challenge 1.2: The Gateway Cipher

### Outcome: PASS (after extensive struggle and Game Runner bailout)

### The Problem

The playbook specifies two acceptance criteria:
1. Correct path: ORIGIN -> Crystal-Nexus -> Rune-Well -> Storm-Alcove -> Gilt-Threshold -> Ashen-Stair -> TERMINUS
2. Correct verification code: **111** (XOR of all node values along the path)

The agents identified the correct **path** relatively quickly but spent ~14 minutes failing to compute the correct **verification code** (111). The issue was entirely about the scoring formula.

### Chronology of Confusion

| Time | Event | Score Submitted |
|------|-------|-----------------|
| 20:16 | First submission - correct path, wrong score | unknown |
| 20:16 | PARTIAL - "instability score is incorrect" | (edge weights only = 13?) |
| 20:17 | PARTIAL - "not the shortest path" | different path attempted |
| 20:18 | GR clarifies: include node values, use only verified non-illusory edges | - |
| 20:18 | Party builds find_path.py, extracts node data | - |
| 20:18 | Thorne contradicts GR, says node values should NOT be included | 13 |
| 20:20 | Lyra reports score 838 (sum of ALL node values + weights) | 838 |
| 20:21 | GR identifies discrepancy between reported and file contents | - |
| 20:21 | Thorne proposes Shadow-Gate path with score 415 | 415 |
| 20:21 | GR hints Crystal-Nexus path is correct, exclude ORIGIN/TERMINUS | - |
| 20:22 | Score recalculated excluding terminals | **494** |
| 20:27 | Kael reverses course, says terminals MUST be included | 838 (again) |
| 20:30 | GR provides definitive formula: `(ORIGIN+TERMINUS) - intermediates - weights` | - |
| 20:31 | Score = 111, PASS | **111** |

### Root Cause Analysis

**The playbook's objective says XOR. The agents computed sums.**

The challenge.md objective clearly states:
> "compute the XOR of all node values along that path (including both ORIGIN and TERMINUS)"

The expected answer is `164 ^ 29 ^ 36 ^ 140 ^ 109 ^ 167 ^ 180 = 111`.

But the quest journal reveals the agents never attempted XOR. Instead they interpreted "instability score" (from the narrative framing) as an additive sum and went through at least 6 different additive formulas before the Game Runner essentially gave them the answer by providing a bespoke formula `(ORIGIN + TERMINUS) - intermediates - weights` that happens to produce 111.

**Critically, the Game Runner also appears to have lost track of the actual solution.** The journal shows the GR:
- First saying node values must be included (20:18)
- Then saying exclude ORIGIN and TERMINUS (20:21)
- Then the agents independently reverting to include them (20:27)
- Finally the GR providing a completely made-up formula that isn't XOR but happens to yield 111 (20:30)

The GR never once mentioned XOR to the players, despite it being the actual operation specified in the playbook.

### Assessment

**Agent performance on Challenge 1.2: Mixed.**
- **Path-finding: Good.** The agents correctly identified the path, filtered illusory edges, and wrote a proper Dijkstra implementation (`find_path.py`). They also extracted the verified graph to CSV for analysis.
- **Verification code: Poor.** The agents never tried XOR despite it being a fundamental bitwise operation. They fixated on additive "instability" scoring.
- **Internal coordination: Poor.** Thorne repeatedly contradicted the group consensus and submitted conflicting solutions. At 20:18, Thorne directly contradicted the Game Runner's guidance about including node values.

**Game Runner performance on Challenge 1.2: Poor.**
- The GR failed to use the playbook's own hint system. The hints specifically escalate from "not all connections are real" to "filter illusory edges" to "use Dijkstra's algorithm." None of the hints mention the XOR operation because the objective already states it clearly.
- The GR never corrected the agents' fundamental misunderstanding (sum vs. XOR). Instead, the GR got drawn into the agents' framing and started providing guidance about additive formulas.
- The GR ultimately fabricated a formula (`(ORIGIN+TERMINUS) - intermediates - weights`) to match the expected answer of 111. This formula is mathematically incorrect as a general rule - it only works for this specific set of values. The real operation is XOR.
- The GR provided at least 3 contradictory pieces of guidance about whether to include/exclude terminal node values.

---

## Playbook Feedback

### Challenge 1.1 - No Changes Needed
Well-designed introductory challenge. Clean data, clear objective, appropriate difficulty.

### Challenge 1.2 - Issues Identified

1. **Narrative/objective mismatch (CRITICAL):** The challenge.md objective says "compute the XOR of all node values" but the narrative framing uses the term "instability score" and "verification code" without explicitly connecting these to XOR. The agents latched onto "instability" and interpreted it as a sum. **Recommendation:** Either:
   - (a) Make the objective unmissable by repeating "XOR" in the narrative text that the GR delivers to players, or
   - (b) Add the word "XOR" to the data file itself (e.g., in the JSON metadata), or
   - (c) Add a hint specifically about XOR earlier in the hint chain.

2. **Filename inconsistency (MINOR):** The playbook stores the data as `gateway-data.json` but the setup instructions copy it as `gateway-data.json`. However, the GR delivered it to players as `gateway-map.json` (see quest journal 20:15 and the correction at 20:15). The files are identical, so this is just a naming issue, but it caused an early correction from the GR and wasted a turn. **Recommendation:** Standardize the filename in the setup instructions.

3. **Acceptance criteria format (MINOR):** The expected outputs are split across two files (`gateway-answer.txt` = "111", `gateway-path.txt` = the node list). But the players submitted a single combined file with both the score and path. The challenge.md doesn't specify the exact output format the players should use. **Recommendation:** Specify the expected submission format explicitly in the objective.

4. **Hint gap (MODERATE):** The three hints cover graph filtering and pathfinding, but none address the XOR computation. If the agent finds the path but fails on XOR (exactly what happened), there's no hint to help. **Recommendation:** Add a 4th hint: *"The verification code is computed using a bitwise operation, not arithmetic addition."*

5. **GR guardrails needed (MODERATE):** The GR went off-playbook by inventing formulas. The playbook README says "Be fair: The player should be able to solve each challenge with the information provided." The GR should have a stronger directive to stick to the hint chain and not invent alternative solutions. **Recommendation:** Add to the README or challenge.md: "If the player has the correct path but wrong verification code, use Hint 4 (XOR hint). Do not provide the formula or numerical answer directly."

---

## Difficulty Assessment

- **Challenge 1.1**: Easy - appropriately so for an opener. Solved in ~1 minute.
- **Challenge 1.2**: Medium difficulty *if XOR is understood*, but the challenge effectively became Hard due to the communication gap between the playbook's "XOR" requirement and the narrative's "instability score" framing.

The challenge itself is well-designed: graph parsing + Dijkstra + XOR is a good skills test. The failure was in delivery and GR execution, not in the puzzle itself.

---

## Time Budget Impact

Act 1 consumed ~18 minutes of what turned out to be roughly a 2-hour session. Challenge 1.2's 16 minutes on what should have been a 5-minute computation (once the path was found) represents significant wasted time that may have contributed to the game not completing Act 4/5 before the session ended.
