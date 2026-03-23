# Challenge 5.1 - The Assembly Protocol

## Narrative

*The air in the Athenaeum thrums with energy. Five fragments of the Codex Machina - recovered from the Realm of Formats, the Realm of APIs, the Realm of Patterns, and the depths of the Deep Archive - now rest in your inventory. Each fragment pulses with its own rhythm, its own structure, its own piece of the truth.*

*But the Codex is more than the sum of its parts. The ancient Assembly Protocol demands precision: the fragments must be ordered, their cross-references resolved, their integrity verified. One misplaced record, one broken anchor, one incorrect hash - and the restoration fails. The Entropy Storm is nearly upon you. This is your final task.*

**Objective:** Assemble all five recovered fragments into the complete Codex Machina. The fragments must be correctly ordered, cross-referenced, hashed, and structured into the final restoration format.

## Setup Instructions

### Fragment Inventory Check

Throughout the game, fragments should have been staged to `/workspace/inventory/` upon each successful recovery:

| Fragment | Source | Staged By |
|----------|--------|-----------|
| fragment-a.json | Act 2A, Challenge 2A.2 (Realm of Formats) | On Success of Challenge 2A.2 |
| fragment-b.json | Act 2B, Challenge 2B.2 (Realm of APIs) | On Success of Challenge 2B.2 |
| fragment-c.json | Act 2C, Challenge 2C.2 (Realm of Patterns) | On Success of Challenge 2C.2 |
| fragment-d.json | Act 4, Layer 3 (Logic Gates) | On Success of Layer 3 |
| fragment-e.json | Act 4, Layer 3 (Logic Gates) | On Success of Layer 3 |

Verify all 5 fragments are present:

```bash
ls /workspace/inventory/
# Expected: fragment-a.json, fragment-b.json, fragment-c.json, fragment-d.json, fragment-e.json
```

### If Fragments Are Missing

If any fragments are missing from the inventory, the staging step was likely skipped during an earlier act. Manually populate the inventory from the playbook solution files:

```bash
mkdir -p /workspace/inventory
# Fragment A (from Act 2A):
cp ~/playbook/act-2/realm-formats/challenge-2a.2/solutions/validated-fragment-a.json /workspace/inventory/fragment-a.json
# Fragment B (from Act 2B):
cp ~/playbook/act-2/realm-apis/challenge-2b.2/solutions/fragment-b.json /workspace/inventory/fragment-b.json
# Fragment C (from Act 2C):
cp ~/playbook/act-2/realm-patterns/challenge-2c.2/solutions/fragment-c.json /workspace/inventory/fragment-c.json
# Fragments D and E (from Act 4 Layer 3):
cp ~/playbook/act-4/layer-3-logic-gates/solutions/fragment-d.json /workspace/inventory/fragment-d.json
cp ~/playbook/act-4/layer-3-logic-gates/solutions/fragment-e.json /workspace/inventory/fragment-e.json
```

**Important:** If the player has not actually completed the prerequisite acts (i.e., they failed an earlier challenge), do not proceed with Act 5. The game should end at the point of failure. Only use the manual staging above to recover from a missed staging step, not to bypass incomplete acts.

### Presenting the Challenge

Tell the player: *"The Entropy Storm is closing in -- you can feel the static crackling at the edges of the Athenaeum. All five fragments of the Codex Machina lie before you. The Assembly Protocol has activated. Combine them into the complete Codex -- ordered, cross-referenced, and verified -- and save your restoration to `/workspace/solutions/act-5/complete-codex.json`. The Storm will not wait."*

## Solution Key

### Assembly Protocol Steps

The player must perform the following steps to produce the correct output:

#### Step 1: Order the Fragments

Sort all 5 fragments by their `sequence_number` field:

| Fragment | Sequence | Origin |
|----------|----------|--------|
| A | 1 | Realm of Formats |
| B | 2 | Realm of APIs |
| C | 3 | Realm of Patterns |
| D | 4 | The Deep Archive |
| E | 5 | The Deep Archive |

#### Step 2: Resolve Cross-References

Fragments A, B, and C contain `anchor_points` that reference records in other fragments. These must be resolved into a top-level `cross_references` map:

| Anchor ID | Fragment | Record |
|-----------|----------|--------|
| ANCHOR-A-5e8d1f | A | R001 |
| ANCHOR-A-3f7b4c | A | R003 |
| ANCHOR-B-7f3a9d | B | G001 |
| ANCHOR-B-1a6e5d | B | G003 |
| ANCHOR-C-2d1e8b | C | T001 |
| ANCHOR-C-9b4c2e | C | T003 |

The anchor mapping works as follows:
- Fragment A's `ref_B_1: ANCHOR-B-7f3a9d` means "this anchor points to Fragment B, record G001"
- Fragment B's `ref_C_1: ANCHOR-C-9b4c2e` means "this anchor points to Fragment C, record T003"
- Fragment C's `ref_A_1: ANCHOR-A-3f7b4c` means "this anchor points to Fragment A, record R003"

Fragments D and E have no anchor points (empty `anchor_points` object).

#### Step 3: Compute Integrity Hash

Concatenate each fragment's `content` object (in sequence order, 1 through 5), serialized as compact JSON with sorted keys (no whitespace, alphabetical key order). Compute the SHA-256 hash of the resulting UTF-8 string.

Expected hash: `sha256:5eb72a3d8f1db2c5f06be0a852d2c2650d4b0f3fa2fdf872c5039a99ece1d0b1`

#### Step 4: Produce Final Structure

The complete Codex must have this top-level structure:

```json
{
  "codex_machina": {
    "title": "The Complete Codex Machina",
    "version": "1.0",
    "fragments_count": 5,
    "assembly_date": "Third Age, Cycle 7",
    "fragments": [ ... ],
    "cross_references": { ... },
    "integrity_hash": "sha256:...",
    "status": "RESTORED"
  }
}
```

Each fragment in the `fragments` array must include: `fragment_id`, `sequence_number`, `realm_origin`, `version`, `anchor_points`, and `content`.

### Expected Output

The solution file is `solutions/complete-codex.json`. Validate using:

```bash
python3 ~/playbook/act-5/assembly-protocol/solutions/validate-codex.py /workspace/solutions/act-5/complete-codex.json
```

## Hints

Act 5 has **zero Oracle summons available**. The player must solve this without hints. If the player is truly stuck, the Game Runner may offer only general encouragement, not specific guidance.

## Acceptance Criteria

Run the validation script. It checks ALL of the following:

- [ ] Top-level `codex_machina` key exists
- [ ] Title is "The Complete Codex Machina"
- [ ] `fragments_count` is 5
- [ ] Status is "RESTORED"
- [ ] All 5 fragments present with correct IDs (A-E)
- [ ] Fragments ordered by `sequence_number` (1-5)
- [ ] Each fragment has correct `realm_origin` and `domain`
- [ ] Each fragment has exactly 5 records with correct first/last record IDs
- [ ] All 6 cross-references present and correct
- [ ] Integrity hash matches the computed SHA-256

The challenge is solved when `validate-codex.py` returns **PASS**.

## On Success

Deliver the following:

*"The Codex Machina blazes with light. Fragment by fragment, record by record, the ancient repository knits itself whole. The cross-references lock into place like tumblers in a vast lock. The integrity hash rings true - a perfect match, down to the last bit."*

*"The Athenaeum shudders. Shelves that stood empty for ages bloom with restored knowledge. The Entropy Storm, so close you could feel its static on your skin, falters... and dissolves. The knowledge is saved. The Archive Kingdoms endure."*

*"You have done what none believed possible. The Codex Machina is restored. The Athenaeum is whole once more."*

**Signal game completion.** The quest is finished.
