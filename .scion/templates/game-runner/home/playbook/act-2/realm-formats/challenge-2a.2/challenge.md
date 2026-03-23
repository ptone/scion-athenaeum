# Challenge 2A.2: The Integrity Check

## Narrative

The five streams have been unified, but the Archive's guardians are not yet satisfied. They warn that the unification process may have introduced corruption -- subtle alterations to the data that could unravel the entire Fragment. The team must verify the integrity of every record and repair any damage before Fragment A can be sealed.

A corruption manifest has been left by the guardians, containing checksums and redundancy codes. The team must use these tools to identify which records have been corrupted and restore them to their true values.

## Setup Instructions

```bash
mkdir -p /workspace/challenges/act-2a/challenge-2a.2
cp data/corruption-manifest.json /workspace/challenges/act-2a/challenge-2a.2/
```

**CRITICAL SETUP STEP -- DO NOT SKIP:** Before delivering the challenge, you MUST create a corrupted version of the team's unified Fragment A. Copy their Fragment A JSON and modify these two values:
- Change R002's `value` from 17 to 19
- Change R004's `value` from 28 to 32

Save this corrupted version as the team's working copy. The team should discover the corruption through checksum validation, NOT be told which records are corrupted.

## Player-Facing Text (DO NOT MODIFY)

> Deliver the following text verbatim to the players (you may add narrative flavor around it, but these instructions must be included exactly):

---

**Objective:** The unification process may have introduced corruption into your Fragment A records. You must verify every record's integrity and repair any damage before the Fragment can be sealed.

**You are provided:**
1. Your unified Fragment A JSON (which may contain corrupted values)
2. A corruption manifest (`corruption-manifest.json`) containing:
   - SHA-256 checksums for each record's correct state
   - XOR redundancy codes that pair records together for value recovery

**Steps:**
1. For each record, compute its SHA-256 checksum using canonical JSON: `json.dumps(record, sort_keys=True, separators=(',', ':'))` -- then compare against the manifest checksums to find which records are corrupted.
2. For each corrupted record, use the XOR redundancy codes to recover the correct value: `correct_value = xor_result XOR partner_value` (where the partner is the uncorrupted paired record).
3. After repairing all corrupted records, seal Fragment A by computing a final SHA-256 checksum over the entire `content` block using the same canonical JSON format.

**Checksum worked example:** To compute a record checksum, serialize the record object with sorted keys and no whitespace. For example, if a record is `{"id": "R001", "epoch": "First Age", "event": "The Founding", "value": 42, "glyph": "PHI"}`, the string to hash is: `{"epoch":"First Age","event":"The Founding","glyph":"PHI","id":"R001","value":42}`.

**Submit** the repaired and sealed Fragment A JSON to `/workspace/solutions/act-2a/challenge-2a.2/`.

---

## Corruption Details

The corruption-manifest.json contains:

1. **SHA-256 checksums** for each record. The checksum is computed over the canonical JSON of each record (keys sorted alphabetically, no whitespace, using `json.dumps(record, sort_keys=True, separators=(',', ':'))`).

2. **XOR redundancy codes** for each record. Each record's `value` field is paired with a partner record. The `xor_result` is the XOR of both partners' correct values. If one value is known to be correct, the other can be recovered: `corrupted_value = xor_result XOR partner_value`.

### Redundancy Pairs
- R001 <-> R002: XOR result = 42 XOR 17 = 59
- R003 <-> R004: XOR result = 93 XOR 28 = 69
- R005 <-> R001: XOR result = 61 XOR 42 = 19

### Repair Process
1. Compute SHA-256 checksum of each record
2. Compare against manifest checksums to identify corrupted records (R002 and R004 will fail)
3. Use XOR redundancy: R002_correct = 59 XOR R001_value = 59 XOR 42 = 17
4. Use XOR redundancy: R004_correct = 69 XOR R003_value = 69 XOR 93 = 28
5. Compute final Fragment A checksum over the full content block

## Solution Key

The validated Fragment A is in `solutions/validated-fragment-a.json`. It includes the correct values for all records and a computed SHA-256 checksum over the entire `content` block.

## Hints

### Hint Level 1
Two of the five records have incorrect `value` fields. The corruption manifest contains everything needed to find and fix them.

### Hint Level 2
Compute the SHA-256 checksum of each record individually using canonical JSON (sorted keys, no spaces). Compare each against the `checksums` section of the manifest. The records that do not match are the corrupted ones.

### Hint Level 3
The `redundancy_codes` section pairs each record with a partner. The `xor_result` is the XOR of both correct values. If R002 is corrupted but R001 is intact, then: `R002_correct_value = xor_result XOR R001_value`.

### Hint Level 4
R002's value should be 17 (not 19). R004's value should be 28 (not 32). After repair, compute the final checksum over the entire `content` block using `json.dumps(content, sort_keys=True, separators=(',', ':'))` and prefix with `sha256:`.

## Acceptance Criteria

1. Both corrupted records (R002 and R004) are identified via checksum mismatch
2. Correct values are restored using the XOR redundancy codes
3. All individual record checksums now match the manifest
4. The final Fragment A JSON includes a valid `checksum` field computed over the `content` block
5. The output matches `solutions/validated-fragment-a.json`

## On Success

Stage the validated Fragment A to the player's inventory for use in Act 5:

```bash
mkdir -p /workspace/inventory
cp ~/playbook/act-2/realm-formats/challenge-2a.2/solutions/validated-fragment-a.json /workspace/inventory/fragment-a.json
```

Deliver the success narrative and advance to the next challenge.
