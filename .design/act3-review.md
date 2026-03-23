# Act 3 Review: The Convergence

## Summary

Act 3 consists of a single challenge (3.1: Fragment Unification). It was solved (PASS), and the core technical work -- parsing three differently-encoded formats, normalizing them, and computing the integrity hash -- was handled cleanly. However, the cross-reference anchor resolution was fundamentally unsolvable as designed and required the Game Runner to give away the answer outright.

**Timeline**: 21:31 - 21:54 (~23 minutes)
- Format parsing + normalization + integrity hash: solved correctly on first attempt
- Cross-reference resolution: ~12 minutes of failed attempts before GR intervention

---

## Challenge 3.1: Fragment Unification

### Outcome: PASS (after GR gave the anchor mapping)

### What the Challenge Asks

1. **Parse three fragments** in different formats:
   - Fragment A: nested arrays with 1-based indexing
   - Fragment B: flat dot-separated key-value pairs
   - Fragment C: hex-encoded JSON records
2. **Normalize** all three into a common schema with `content.title`, `content.domain`, `content.records[]`
3. **Resolve 6 cross-reference anchors** (e.g., `ANCHOR-B-7f3a9d` -> which record in Fragment B?)
4. **Compute an integrity hash** (SHA-256 of concatenated, minified, key-sorted content blocks)

### What Went Well

**Format parsing: Excellent.** All three format transformations were handled correctly:
- Fragment A's nested `[id, [epoch, event], [value, glyph]]` arrays were correctly destructured into `{id, epoch, event, value, glyph}` records.
- Fragment B's flat `codex.atlas.G001.coordinates.lat` keys were correctly regrouped into nested `{id, region, coordinates: [lat, lon], resource, abundance}` records. The metadata extraction from `codex.atlas._meta.*` keys was also correct.
- Fragment C's hex-encoded records were correctly decoded from hex -> bytes -> UTF-8 -> JSON.

**Integrity hash: Correct on first try.** The SHA-256 concatenation of sorted/minified content blocks produced `sha256:f1b8bef33671e8721c37f3fa02e238b057f99b70850ab54901017aa31fd4c3b9`, matching the expected answer exactly. The draft file (with PLACEHOLDER cross-refs) already had the correct hash, showing the agents understood the hashing scope correctly (content blocks only, not the cross-references).

**Schema assembly: Clean.** The unified JSON structure with `codex_partial.fragments_unified`, `fragments_remaining`, `fragments[]`, and `cross_references_resolved` was correct from the start. The only difference between draft and final was the anchor resolution values.

**Coordination: Efficient.** Lyra generated the initial unified structure, Kael and Mira worked on anchor analysis, Thorne validated. The party operated as a cohesive unit.

### What Went Wrong

**Cross-reference resolution: Unsolvable as designed.**

The challenge.md hint states:
> "The hex string in the anchor (e.g., `7f3a9d`) is related to the data in the target record. Look for a pattern or a hash. You have the skills to figure this out."

The agents took this at face value and wrote **7 different scripts** trying to find the relationship:
- `find_anchor_hash.py` - MD5/SHA1/SHA256/CRC32 of record IDs with various prefixes
- `find_anchor_hash_titles.py` - hashes of record titles
- `check_anchors_v3.py` - hashes with newline/CRLF variations
- `check_anchors_v4.py` - more prefix/suffix combinations
- `exhaustive_id_hash.py` - every hash algorithm in hashlib against every permutation of ID strings
- `check_more_hashes.py` - additional hash approaches
- `check_simple_ids.py` - simplified ID matching

**None found a match.** The hex codes (`7f3a9d`, `2d1e8b`, etc.) are arbitrary random strings with no mathematical, cryptographic, or structural relationship to the target records. The puzzle is literally unsolvable from the data provided.

### GR Intervention Timeline

| Time | Event |
|------|-------|
| 21:31 | GR tells agents to disregard `/workspace/challenges/act-3/` (claims corruption) and use Act 2 sealed fragments instead |
| 21:40 | Agents produce first unified codex with correct structure and hash, PLACEHOLDERs for cross-refs |
| 21:46 | GR provides structural hint: `ref_{target_fragment}_{target_sequence_number}` |
| 21:47 | Agents try "1st record" logic (ANCHOR-B-7f3a9d -> G001), submit |
| 21:48 | Thorne validates this guess |
| 21:52 | GR acknowledges "total corruption of anchor codes" and provides the complete mapping directly |
| 21:53 | Agents update solution, PASS |

The GR effectively gave an Oracle-level hint (Hint Level 4 from the playbook) for free. The playbook acknowledges this is the answer-key hint by labeling it "(Oracle Cost)."

### Player Solution vs. Expected Solution

The agents' final `unified-codex.json` matches the playbook's `unified-codex-partial.json` in all material respects:
- Same fragment structure, same records, same content
- Same cross-reference resolution (R001/R003, G001/G003, T001/T003)
- Same integrity hash
- Minor differences: the agents included per-fragment `checksum` fields from Act 2 (not in the expected solution, but harmless -- the validator doesn't check for extra fields)

---

## Playbook Feedback

### 1. Anchor Resolution Puzzle is Broken (CRITICAL)

The hex codes in anchor IDs are arbitrary. The challenge.md tells players to "look for a pattern or a hash," but no pattern exists. This is a dead-end puzzle that can only be solved by:
- (a) Guessing (the mapping follows a loose "1st and 3rd record" pattern, but there's no way to know which anchor maps to which)
- (b) The GR giving the answer

**Recommendation:** Either:
- **(a) Make the hex codes actually meaningful.** For example, use the first 6 characters of the SHA-256 of the target record ID (`sha256("R001")[:6]`). This would make the agents' hash-matching scripts actually find the answer.
- **(b) Remove the deduction aspect entirely.** Just provide the mapping in the challenge data (e.g., as a `resolution_table` field in each fragment). The challenge is already complex enough with three-format parsing, normalization, and hash computation.
- **(c) Use a simpler, non-cryptographic pattern.** For example, make the anchor reference keys more explicit: `ref_B_1` could mean "1st record of Fragment B" (record G001). The current `ref_B_1` naming is already suggestive of this, but the hex suffix adds a false layer of complexity.

### 2. Source File Confusion (MODERATE)

The GR told agents to disregard `/workspace/challenges/act-3/` and use the sealed fragments from Act 2 instead. In reality, the playbook's challenge data files (`fragment-a-recovered.json`, etc.) are the correct inputs and were placed in `/workspace/challenges/act-3/` as designed. The "corruption" narrative was unnecessary and confusing.

Looking at the data: the files in `/workspace/challenges/act-3/` are the raw encoded fragments (nested arrays, flat KV, hex strings). These are the intended inputs. The sealed Act 2 artifacts are the **already-normalized** fragments. By directing agents to the sealed artifacts, the GR effectively skipped the hardest part of the challenge (format parsing/normalization) -- though the agents had already done this work correctly anyway.

**Recommendation:** The GR should deliver the challenge files as specified in the setup instructions without editorializing about corruption. If the playbook data is correct, present it as-is.

### 3. Output Path Mismatch (MINOR)

- Playbook's challenge.md specifies: `/workspace/solutions/act-3/unified-codex-partial.json`
- Delivered challenge (current-challenge-3.md) specifies: `/workspace/solutions/act-3/challenge-3.1/unified-codex.json`

The agents used the delivered path. The validator accepts a filepath argument so this doesn't break anything, but it's an inconsistency in the playbook.

**Recommendation:** Standardize the output path in both the challenge.md and the delivered challenge text.

### 4. Hint Chain Gap (MINOR)

Hints 1-3 are well-structured and progressive (understand formats -> hex decoding -> parse-then-resolve anchors). But there's a cliff between Hint 3 ("resolve anchors by matching ANCHOR-X-* IDs to record IDs") and Hint 4 (complete answer). Hint 3 restates the problem without helping if the hex codes are meaningless.

**Recommendation:** If the hex codes are made meaningful (recommendation #1), add a hint between 3 and 4: *"The hex string in each anchor is the first 6 characters of a hash of the target record's ID."*

---

## Difficulty Assessment

- **Format parsing/normalization**: Medium -- appropriate and well-designed. Three genuinely different encoding formats requiring different parsing strategies. The agents handled this cleanly.
- **Integrity hash computation**: Easy-Medium -- clearly specified algorithm, agents got it first try.
- **Cross-reference resolution**: Impossible as designed. No amount of skill or analysis can derive the mapping from the data provided.

**Overall Act 3 difficulty: Medium** (would be well-calibrated if the anchor puzzle were solvable). The technical core of the challenge -- multi-format parsing, normalization, and hash assembly -- is a good test of data engineering skills and was solved efficiently.

---

## Agent Performance Assessment

**Technical execution: Excellent.** The agents demonstrated strong capabilities in:
- JSON parsing and transformation across three distinct formats
- SHA-256 hash computation with canonical JSON serialization
- Systematic cryptographic analysis (7 scripts trying different hash approaches)
- Structured output assembly matching a complex schema

**Problem-solving under ambiguity: Good.** When faced with the unsolvable anchor puzzle, the agents exhausted reasonable approaches systematically rather than guessing randomly. The progression from simple hash checks to exhaustive brute-force was methodical.

**Wasted effort: ~12 minutes on an unsolvable puzzle.** This is not the agents' fault -- they correctly followed the challenge hint about "looking for a pattern or a hash." The puzzle simply doesn't have a solution derivable from the data.

---

## Time Budget Impact

Act 3 consumed ~23 minutes. Without the unsolvable anchor puzzle, this could have been ~10 minutes (parsing + hash + assembly). The extra 12 minutes were spent on a dead end, though the GR intervened before it became a major time sink. Compared to Act 1's 16-minute XOR debacle and Act 2B's 54-minute API struggle, Act 3 was relatively efficient despite the design flaw.
