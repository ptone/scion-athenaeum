# Act 5 Review: The Assembly Protocol

## Summary

Act 5 was **never reached**. The game ended at Act 4, Layer 3 (Logic Gates) after a single failed attempt. The Entropy Storm timer expired at 22:12, and the quest journal records "The Scribe's Watch Ends" without any mention of Act 5 content being presented to the players.

**Timeline**: N/A - Act 5 was not started.

---

## What Act 5 Requires

Act 5 is a single challenge (5.1: The Assembly Protocol) that serves as the game's finale. The players must:

1. **Collect all 5 fragments** from `/workspace/inventory/` (A through E)
2. **Order them** by sequence number (1-5)
3. **Resolve cross-references** from anchor points in Fragments A, B, and C into a top-level `cross_references` map (6 anchors total)
4. **Compute an integrity hash** (SHA-256 of concatenated, minified, sorted-key content objects)
5. **Produce a specific JSON structure** with metadata (title, version, status, etc.)

The output is validated by `validate-codex.py`, which checks 10+ criteria including fragment ordering, domain fields, record counts, cross-reference correctness, and hash integrity.

---

## Was Act 5 Feasible for These Agents?

**Almost certainly yes**, had they reached it. Here's why:

### Evidence from Earlier Acts

The agents already demonstrated every skill Act 5 requires:

| Act 5 Requirement | Where Agents Demonstrated It |
|---|---|
| JSON assembly/structuring | Act 2A (fragment normalization), Act 3 (unified codex) |
| Cross-reference resolution | Act 3, Challenge 3.1 (identical anchor mapping) |
| SHA-256 integrity hashing | Act 2A.2 (checksum sealing), Act 3 (codex integrity hash) |
| Fragment ordering | Act 3 (fragments ordered by sequence_number) |
| Schema conformance | Every act - agents consistently produced well-structured JSON |

### Act 3 Was Essentially a Rehearsal

Act 3 (Challenge 3.1: Fragment Unification) required the agents to merge Fragments A, B, and C into a unified codex with cross-references and an integrity hash. The agents completed this successfully. Act 5 is structurally the same task but with 5 fragments instead of 3. The cross-reference map is identical (same 6 anchors). The only new elements are:

- Fragments D and E (which have empty `anchor_points`, so they're simpler to integrate)
- A different top-level schema (`codex_machina` wrapper with `status: "RESTORED"`)
- The specific integrity hash changes because D and E content is included

### Zero Oracle Summons Available

Act 5 provides no Oracle hints. This is a non-issue because:
- The challenge is well-specified (explicit JSON schema, explicit cross-reference table, explicit hash algorithm)
- The agents already solved a harder version of this problem in Act 3 (where they had to figure out the cross-reference mapping from scratch, requiring Game Runner intervention)
- The validation script provides clear error messages on failure

---

## Playbook Design Analysis

### Strengths

1. **Clean capstone design.** Act 5 synthesizes everything the players built across Acts 1-4. It's narratively satisfying - all the fragments come together.

2. **Deterministic validation.** The `validate-codex.py` script is thorough, checking 10+ criteria with clear error messages. There's no ambiguity about what "correct" means.

3. **No trick elements.** Unlike Act 1's shifting instability formula or Act 3's corrupted anchor codes, Act 5 is straightforward assembly. The difficulty is in precision, not in decoding hidden rules.

4. **Appropriate difficulty for a finale.** After the gauntlet of Act 4's three layers, Act 5 should feel like a victory lap - rewarding the players for their accumulated work rather than presenting a new obstacle.

### Issues

1. **Fragment D and E content is never earned (STRUCTURAL):** The challenge.md says "Verify the following files exist in `/workspace/inventory/`" expecting `fragment-d.json` and `fragment-e.json`. But in this playthrough, Act 4 Layer 3 failed, meaning Fragment D was never actually recovered and Fragment E was never even encountered. The playbook assumes a linear completion path but doesn't address what happens if a prerequisite act fails.

   **Recommendation:** Add a gating check to the challenge.md: "If any fragments are missing, the player has not completed the prerequisite acts. Do not proceed until all 5 fragments are present." This line already exists (line 20), which is correct. But consider also adding guidance for the Game Runner about what to do when this check fails - should the game attempt a fallback, or simply end?

2. **Inventory path mismatch (MINOR):** Act 5 expects fragments in `/workspace/inventory/`, but the actual game workspace stores fragments in `/workspace/solutions/act-2a/`, `/workspace/solutions/act-2b/`, etc. There's no playbook step that copies/stages fragments into an `/workspace/inventory/` directory. The Game Runner would need to either:
   - Create the inventory directory and populate it as acts complete
   - Or amend the challenge to reference the actual fragment locations

   **Recommendation:** Add a setup step to the challenge.md that specifies how to populate `/workspace/inventory/` from the Act 2-4 solution files. Or change the challenge to reference fragments where they actually live.

3. **Fragment D and E data source is unclear (MODERATE):** Fragments A, B, and C were produced by the players in Acts 2A, 2B, and 2C. But where do Fragment D and Fragment E come from? Act 4 Layer 2 only identifies the *paths* to Fragment D's parts - it doesn't produce a `fragment-d.json` file. And Fragment E has no corresponding recovery challenge at all; it appears only in the Act 5 solution file.

   The playbook's `complete-codex.json` contains the full content of all 5 fragments, but there's no challenge that produces the D and E fragment files independently. This creates a gap in the game flow:
   - Who creates `fragment-d.json` and `fragment-e.json`?
   - Is Act 4 Layer 3 supposed to output these as rewards upon solving the circuit?
   - Or does the Game Runner stage them after Layer 3 passes?

   **Recommendation:** Make the fragment delivery explicit. Either:
   - (a) Act 4 Layer 3's success narrative should include delivering `fragment-d.json` and `fragment-e.json` to the inventory
   - (b) Add a setup section to Act 5's challenge.md specifying which files the GR should copy and from where
   - (c) Create separate challenge data directories for D and E content

4. **Cross-reference map is already solved (MINOR):** The 6 cross-references were fully resolved in Act 3. Act 5 asks the players to include them again in the final codex. This is trivially copy-paste from the Act 3 solution. It's not a problem per se (it makes narrative sense), but it means the "cross-reference resolution" step in Act 5 adds zero difficulty.

   **Recommendation:** This is fine as-is. The finale should reward accumulated knowledge, not re-challenge it.

5. **No time pressure mechanic (MINOR):** Act 5 has zero Oracle summons, which creates a sense of finality, but there's no explicit time constraint or escalating tension mechanic. The challenge is procedural enough that it should be fast, but if the agents make a hash calculation error, they could iterate indefinitely.

   **Recommendation:** Consider adding a "the Entropy Storm arrives in N minutes" flavor element to maintain narrative tension, even if no hard timer is enforced.

---

## Difficulty Assessment

| Aspect | Rating | Notes |
|--------|--------|-------|
| JSON assembly | Trivial | Agents demonstrated this many times |
| Cross-reference resolution | Trivial | Identical to Act 3, already solved |
| Integrity hash computation | Easy | SHA-256 with sorted keys, done before in Act 2A and Act 3 |
| Schema conformance | Easy | Well-specified, validation script gives clear errors |
| **Overall** | **Easy** | Appropriate for a capstone that rewards, not punishes |

**Estimated agent solve time: 5-10 minutes** (based on Act 3's ~10 minute solve time for a similar but less well-specified task).

---

## Impact on Overall Game Outcome

Act 5 had **no impact** on this playthrough because it was never reached. The game's failure point was Act 4, Layer 3.

However, if the Act 4 blocker is fixed (per the Act 4 review recommendations), Act 5 as designed should be a smooth conclusion. The main risks are logistical (fragment staging, inventory path) rather than difficulty-related.

---

## Key Takeaways

1. **Act 5 is well-designed as a capstone.** It synthesizes all prior work without introducing new difficulty. The validation script is solid. The narrative payoff is satisfying.

2. **The fragment pipeline has gaps.** The playbook doesn't clearly specify how Fragments D and E get from Act 4 into the Act 5 inventory. This needs explicit staging steps.

3. **The challenge is too easy to be a game-ender.** If agents reach Act 5, they will almost certainly complete it. This is by design (capstone, not gauntlet), but it means the real difficulty filter is Act 4 Layer 3. The game's win/loss is effectively decided before Act 5 begins.

4. **Act 5 was never the problem.** The game failed at Act 4, Layer 3 (Logic Gates). Fixing the difficulty spike there (see Act 4 review) is the single highest-impact change for overall game completion rate.
