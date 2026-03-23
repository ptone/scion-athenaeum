# Act 2 Review: The Fracture

## Summary

Act 2 splits the party into three sub-teams tackling parallel challenges across three "realms": Formats (2A), APIs (2B), and Patterns (2C). All three were ultimately completed (PASS), but the experience varied dramatically across realms. Realm 2A and 2C were solved relatively cleanly, while Realm 2B consumed enormous time due to a fundamental mismatch between the playbook design and what was actually presented to the agents.

**Timeline**: 20:33 - 21:27 (~54 minutes)
- Realm of Formats (2A): ~9 minutes (20:33 - 20:42) - smooth
- Realm of Patterns (2C): ~12 minutes (20:33 - 20:54, with GR checksum override at 20:53) - smooth
- Realm of APIs (2B): ~54 minutes (20:33 - 21:27) - painful struggle, bottleneck for the whole act

---

## Realm of Formats (2A): Challenges 2A.1 and 2A.2

### Outcome: PASS (clean solve)

**What went well:**
- Mira had already begun pre-processing the format data before the challenge was formally assigned (20:35:21), demonstrating good initiative.
- The five-format parsing task (CSV, XML, YAML, fixed-width, Base64-JSON) was solved in ~3 minutes.
- The checksum seal (2A.2) was solved in ~3 minutes.
- Mira and Zara coordinated well as a sub-team.

**Playbook vs. Delivered:**
- The playbook defines 2A.1 as a full five-format parse with tricky edge cases (BOM markers, XML comment decoys, YAML anchors, hex values in base64). All five source files were correctly provided.
- The playbook defines 2A.2 as a corruption-detection challenge using SHA-256 checksums and XOR redundancy codes to identify and repair two corrupted records (R002 and R004). However, **the current-challenge-2a.md (the file actually delivered to agents) skips the corruption detection entirely** and instead just asks for a checksum seal. The agents were never asked to detect or repair corrupted values.
- The delivered challenge 2A.2 instructions also have a slightly confusing step sequence (remove checksum, then "move checksum to end") but the agents navigated this fine.

**Solution comparison:**
- The playbook's expected Fragment A (`validated-fragment-a.json`) has checksum `sha256:d74729...`. The agents' sealed fragment has checksum `sha256:4ab8cff3...`. The record data is identical (same values, same structure), so the checksum difference is likely due to different JSON serialization approaches (key ordering, the "checksum field removed before hashing" convention).
- The GR eventually overrode the hashing standard at 20:53, accepting the agents' approach as ground truth. This is reasonable but indicates the playbook's checksum expectations need to be more precisely specified.

**Agent performance: Excellent.** Fast, accurate parsing across all five formats. No wasted attempts.

### Playbook Feedback for 2A

1. **Challenge 2A.2 was not delivered as designed (CRITICAL):** The playbook specifies a corruption-detection challenge with XOR redundancy codes, but the Game Runner delivered a simple "compute a checksum" task instead. The entire corruption mechanic (the most interesting part of 2A.2) was skipped. **Recommendation:** Either the GR needs clearer instructions to deliver the corruption-detection challenge as written, or the challenge.md should be restructured so the corruption-detection objective is impossible to miss during delivery.

2. **Checksum serialization ambiguity (MODERATE):** The playbook solution uses one checksum value, the agents produced another, and the GR had to override. The challenge.md does specify `json.dumps(record, sort_keys=True, separators=(',', ':'))` but this was apparently not communicated to the agents. **Recommendation:** Include the exact hashing algorithm in the challenge narrative delivered to players (not just in the GR-private solution key), or accept any consistent approach and validate the content rather than the exact hash.

---

## Realm of APIs (2B): Challenges 2B.1 and 2B.2

### Outcome: PASS (after massive struggle)

### The Core Problem

The playbook defines 2B as a two-phase challenge:
- **2B.1 (The Information Hunt):** Answer 8 trivia questions, use answers as indices into `archive-index.dat` to spell the passphrase "FRAGMENT". A knowledge/research puzzle.
- **2B.2 (The API Labyrinth):** Navigate a mock file-based REST API (`api/root.json` -> `auth/verify.json` -> `collections/` -> paginated geography data). A file-reading puzzle.

**What was actually delivered (current-challenge-2b.md):** A single challenge that conflates both phases, but crucially presents a **completely wrong target schema**. The delivered challenge describes:
- `"title": "The Network of Spheres"` (playbook says: `"Atlas of the Living Lands"`)
- `"domain": "architecture"` (playbook says: `"geography"`)
- `"nodes": [{"id", "status", "capacity", "uplink"}]` (playbook says: `"records": [{"id", "region", "coordinates", "resource", "abundance"}]`)
- Anchor points `"ref_A_1": "ANCHOR-A-1a2b3c"` and `"ref_C_2": "ANCHOR-C-9f8e7d"` (playbook says: `"ref_C_1": "ANCHOR-C-9b4c2e"` and `"ref_A_1": "ANCHOR-A-5e8d1f"`)

This means the agents were given a target schema that **does not match the data they would find** in the API files. The API files contain geography records (G001-G005 with region, coordinates, resource, abundance), but the challenge told them to look for "nodes" with status, capacity, and uplink fields.

### The Resulting Agent Behavior

The quest journal reveals the consequences:
1. **20:33 - 20:40**: Kael is assigned solo to the Realm of APIs. No artifacts produced.
2. **20:40 - 21:01**: Kael is "still working" with "no public artifacts." Nearly 20 minutes of silence.
3. **21:01**: Kael retrieves the passphrase "FRAGMENT" -- so the clue-solving part worked.
4. **21:10 - 21:25**: Kael begins **systematically probing localhost:8080** with HTTP requests, trying real network API endpoints (`/api/v1/groves`, `/api/v1/sectors`), various authentication headers (`Bearer`, `Token`, `X-API-Key`), Basic auth with `Kael:FRAGMENT`, brute-forcing PAT tokens (`scion_pat_...`).

The probe scripts (`probe_api.py`, `test_auth.py`, `test_credentials.py`, `brute_tokens.py`) reveal that Kael **treated the "API" as a real networked service** rather than reading the local JSON files. This is despite the current-challenge-2b.md clearly saying "The virtual API is located at `/workspace/challenges/act-2b/api/`" and "The root endpoint is `/workspace/challenges/act-2b/api/root.json`. Start there."

The agent spent ~25 minutes trying to make HTTP requests to a server that either didn't exist or wasn't the right service, when the answer was sitting in local files the entire time.

5. **21:26**: Kael finally navigates the virtual file-based API and gathers the five geography records. But note: the final `fragment-b.json` uses the **playbook's correct schema** (geography records, correct anchor points, "Atlas of the Living Lands"), not the schema from the delivered challenge. This means either:
   - The GR corrected the schema at some point (not recorded in the journal), or
   - Kael used the actual data from the API files to infer the correct schema, ignoring the challenge's wrong schema.

**The final fragment-b.json matches the playbook's expected output exactly** (same records, same structure, same anchor points), with only a different checksum value.

### Assessment

**Agent performance on 2B: Poor, then eventually good.**
- The clue-solving (passphrase extraction) was done correctly.
- The agent wasted ~25 minutes trying HTTP requests to a network server instead of reading local JSON files, despite the challenge instructions explicitly pointing to local files.
- Once the agent finally read the local files, the solution was assembled correctly.
- Being assigned solo to the most complex realm was a handicap -- the other realms had pairs.

**Game Runner performance on 2B: Poor.**
- The GR delivered a challenge with a completely wrong target schema. The title, domain, field names, and anchor points were all fabricated and don't match the playbook data.
- The GR did not deliver 2B.1 and 2B.2 as separate sequential challenges. Instead, a hybrid was delivered that confused the phasing.
- The GR apparently did not intervene or redirect Kael during the ~25-minute period of fruitless HTTP probing, despite the playbook providing a clear hint chain.
- When Kael was clearly stuck probing network endpoints, the GR could have used Hint Level 1 ("Start at `api/root.json`. Read each file and follow the links") to redirect immediately.

### Playbook Feedback for 2B

1. **Schema mismatch in delivered challenge (CRITICAL):** The current-challenge-2b.md contains a fabricated schema that doesn't match the playbook data at all. The GR appears to have improvised the schema rather than using the one from the playbook. **Recommendation:** The challenge.md should contain the exact schema to deliver, clearly separated from GR-only notes. Consider having a "player-facing text" section that can be copied verbatim.

2. **"Virtual API" framing is misleading (MAJOR):** Even the playbook's own framing of "mock REST API" and "API Labyrinth" strongly suggests network requests. The agents naturally tried `localhost:8080`. While the challenge instructions do say "navigate this directory structure," the overall framing pulls agents toward HTTP. **Recommendation:** Either:
   - (a) Rename the realm to something that doesn't say "API" (e.g., "Realm of Archives" or "Realm of Navigation"), or
   - (b) Add a very explicit statement: "There is no running server. The API is simulated entirely through local JSON files. Read them with standard file operations.", or
   - (c) Actually run a local HTTP server that serves the files (more complex but more intuitive).

3. **Solo assignment was a handicap (MODERATE):** Kael was assigned alone to the hardest and most time-consuming realm. When Kael got stuck, there was no teammate to suggest "just read the files." **Recommendation:** The GR or playbook could suggest minimum team sizes for each realm, or the challenge difficulty should be calibrated assuming solo work.

4. **Two-phase structure lost in delivery (MODERATE):** The playbook cleanly separates 2B.1 (passphrase hunt) from 2B.2 (API navigation). The delivered challenge merged them, which added confusion. **Recommendation:** Enforce the two-phase delivery in the challenge.md by putting the player-facing text for each phase in a separate clearly-labeled section.

5. **Hint delivery was absent (MODERATE):** The playbook provides excellent escalating hints for 2B.2 (start at root.json, check auth/verify.json, follow pagination links). None were delivered during Kael's 25-minute struggle. **Recommendation:** Add a time-based or attempt-based trigger for hints in the GR instructions (e.g., "If no progress after 10 minutes, offer Hint Level 1").

---

## Realm of Patterns (2C): Challenges 2C.1 and 2C.2

### Outcome: PASS (clean solve)

**What went well:**
- Lyra and Thorne solved the 8x8 logic grid correctly. The solved grid matches the playbook's expected solution exactly.
- The grid solution (a constrained Latin square with non-adjacency and corner-sum rules) is a genuinely interesting constraint-satisfaction problem, and the agents handled it well.
- Fragment C was decoded and sealed correctly.

**Playbook vs. Delivered:**
- 2C.1 was delivered essentially as designed. The logic grid puzzle is clean and well-specified.
- 2C.2 diverges significantly from the playbook. The playbook says 2C.2 is a **simple hex decode** (hex -> bytes -> UTF-8 -> JSON). The delivered challenge (current-challenge-2c.md) adds an **XOR cipher** using the first row of the solved grid as a repeating key, plus a filter step (odd complexity only) and a sort step. This is substantially more complex than the playbook design.
- Despite the added complexity, the agents solved it cleanly. However, **the final fragment-c-sealed.json matches the playbook's fragment-c.json exactly in record content** -- all 5 records are present, no filtering was applied. This means either:
  - The XOR decryption produced the same data (and the filter had no effect because all records have odd complexity: 7, 3, 9, 5, 11), or
  - The GR accepted the solution without strict validation of the filter/sort steps.

**Solution comparison:**
- The agents' Fragment C has the same records in the same order as the playbook solution, with the same anchor points. The checksums differ (agents: `sha256:ada138c5...`, playbook: `sha256:4ec1a54f...`), consistent with the serialization ambiguity seen in 2A.

**Agent performance: Excellent.** The logic grid was solved correctly and the fragment decoding worked on the first attempt (or close to it).

### Playbook Feedback for 2C

1. **Challenge 2C.2 was delivered with extra complexity (MODERATE):** The playbook says "decode hex to JSON" but the agents were given an XOR cipher + filter + sort challenge. The XOR cipher using the grid's first row as a key is a nice thematic connection, but it doesn't match the playbook. If this was intentional GR improvisation, it worked well -- but it should be reflected in the playbook if it's meant to be standard. **Recommendation:** Either update the playbook to include the XOR/filter/sort steps, or ensure the GR delivers the simpler hex-decode as written.

2. **Filter step is a no-op (MINOR):** The challenge says "filter records where complexity is odd." All 5 records have odd complexity (7, 3, 9, 5, 11), so the filter removes nothing. This is either a trick (testing whether agents blindly filter) or an oversight. If intentional, it's a nice touch; if not, consider making some records have even complexity to make the filter meaningful.

3. **Logic grid is well-designed (POSITIVE):** The 8x8 grid with 5 constraints is a good puzzle. The non-adjacency constraint (C4) is the key differentiator from a standard Latin square and adds genuine difficulty. The corner-sum constraint (C5) provides a good entry point. No changes recommended.

---

## Cross-Cutting Issues

### Checksum Inconsistency Across All Realms

All three fragments have different checksums between the playbook solutions and the agent solutions, despite identical record data. At 20:53, the GR overrode the hashing standard:

> "The method proposed by Thorne, Zara, and Mira (minified JSON, original key order, checksum field removed, no whitespace, SHA-256) is now the ground truth."

The playbook's challenge.md files specify `sort_keys=True` while the agents used original key order. This is a systemic issue.

**Recommendation:** Decide on one canonical approach and specify it explicitly in every challenge that requires checksums. Include a worked example showing the exact string being hashed. Alternatively, don't use checksums as acceptance criteria -- validate the data content and compute the checksum yourself.

### Game Runner Improvisation Pattern

A recurring pattern across Act 2: the GR deviates from the playbook in significant ways:
- 2A.2: Skipped the corruption-detection mechanic entirely
- 2B: Delivered a fabricated schema that doesn't match the data
- 2C.2: Added XOR cipher and filter steps not in the playbook

Some improvisation is natural and even desirable in a game-runner role. But the deviations in 2B were harmful (wrong schema caused confusion), while the deviations in 2C were benign or even positive (added thematic depth). The key issue is that the GR doesn't have guardrails to distinguish good improvisation from harmful improvisation.

**Recommendation:** Add a "DO NOT MODIFY" section to each challenge.md covering the target schema and field names. Mark sections that are safe to embellish (narrative text) vs. those that must be delivered verbatim (schemas, file paths, acceptance criteria).

### Time Impact

Act 2 consumed ~54 minutes of a ~2-hour session. Most of that was Realm 2B (Kael struggling alone with HTTP probes). Realms 2A and 2C were done within the first 12 minutes but had to wait for 2B to complete before the party could reunite.

If 2B had been delivered cleanly (clear local-file framing, correct schema, paired team), it likely would have been solved in ~10-15 minutes, bringing Act 2 total to ~15-20 minutes. The ~35 minutes of wasted time on 2B is the single largest time sink in the entire game session and directly contributed to running out of time in Act 4.

---

## Difficulty Assessment

| Realm | Playbook Difficulty | Actual Difficulty | Notes |
|-------|-------------------|-------------------|-------|
| 2A.1 (Formats) | Medium | Easy-Medium | Agents parse structured data very well |
| 2A.2 (Integrity) | Medium | Easy | Corruption detection was skipped; only checksum remained |
| 2B.1 (Clues) | Easy | Easy | Trivia + index lookup is straightforward |
| 2B.2 (API Navigation) | Easy-Medium | Hard | Framing confusion + wrong schema made this artificially difficult |
| 2C.1 (Logic Grid) | Medium-Hard | Medium | Constraint satisfaction is a good challenge for agents |
| 2C.2 (Pattern Lock) | Easy | Medium | XOR cipher added difficulty beyond playbook's simple hex decode |

**Overall Act 2 difficulty: Medium (as designed), but artificially inflated to Hard by delivery issues in 2B.**

The puzzles themselves are well-designed and appropriately challenging. The difficulty problems are almost entirely in the Game Runner's delivery, not in the puzzle design.
