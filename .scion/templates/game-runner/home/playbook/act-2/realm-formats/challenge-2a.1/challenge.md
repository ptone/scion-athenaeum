# Challenge 2A.1: The Format Gauntlet

## Narrative

The first gate of the Realm of Formats stands before the seekers -- a chamber of five pillars, each humming with a different frequency. Five data streams flow from the pillars, each carrying the same ancient records but speaking in entirely different tongues. The records chronicle the Chronicles of the First Age: five entries that detail the founding events of the Archive.

To pass through the gate, the team must unify these five disparate streams into a single, coherent Fragment -- Fragment A of the Athenaeum.

## Setup Instructions

```bash
mkdir -p /workspace/challenges/act-2a/challenge-2a.1
cp data/fragment-csv.csv /workspace/challenges/act-2a/challenge-2a.1/
cp data/fragment-xml.xml /workspace/challenges/act-2a/challenge-2a.1/
cp data/fragment-yaml.yaml /workspace/challenges/act-2a/challenge-2a.1/
cp data/fragment-fixed.txt /workspace/challenges/act-2a/challenge-2a.1/
cp data/fragment-binary.b64 /workspace/challenges/act-2a/challenge-2a.1/
```

Provide all five files to the team simultaneously. Their task is to produce a unified JSON document containing 5 records with the fields: `id`, `epoch`, `event`, `value` (integer), and `glyph`.

## Data File Descriptions

1. **fragment-csv.csv** -- Semicolon-delimited CSV with a UTF-8 BOM marker. Field names are `record_id`, `age`, `description`, `num`, `symbol`. Some fields contain leading/trailing whitespace. One record contains a quoted field with an embedded semicolon.

2. **fragment-xml.xml** -- XML using a custom namespace `xmlns:codex="urn:archive:codex:v1"`. All data fields are attributes prefixed with `codex:`. Includes XML comments that appear to be data records but are not (decoy entries and misleading record counts).

3. **fragment-yaml.yaml** -- YAML using anchors (`&`) and aliases (`*`) for shared metadata. Field names are `identifier`, `period`, `description`, `magnitude`, `sigil`. Contains metadata cross-references that must be ignored when extracting core record data.

4. **fragment-fixed.txt** -- Fixed-width columnar data with NO header row. Column layout: ID (4 chars), EPOCH (12 chars), EVENT (35 chars), VALUE (5 chars, right-aligned), GLYPH (8 chars). Column positions must be inferred.

5. **fragment-binary.b64** -- Base64-encoded JSON payload. When decoded, it contains a list of objects with abbreviated field names: `i` (id), `e` (epoch), `v` (event), `n` (value as hex string), `g` (glyph).

## Solution Key

The unified output must match the structure in `solutions/unified-fragment-a-raw.json`. The Fragment A schema is:

```json
{
  "fragment_id": "A",
  "sequence_number": 1,
  "realm_origin": "Realm of Formats",
  "version": "1.0",
  "checksum": "sha256:to_be_computed",
  "anchor_points": {
    "ref_B_1": "ANCHOR-B-7f3a9d",
    "ref_C_1": "ANCHOR-C-2d1e8b"
  },
  "content": {
    "title": "Chronicles of the First Age",
    "domain": "history",
    "records": [ ... 5 records ... ]
  }
}
```

Each record has: `id`, `epoch`, `event`, `value` (integer), `glyph`.

## Hints

### Hint Level 1
Each data file contains the same 5 records. Start by parsing the CSV -- it has labeled columns that will help you identify the field mapping for the other formats.

### Hint Level 2
The CSV uses semicolons as delimiters, not commas. Watch out for the BOM marker at the start of the file and for a record with a semicolon inside a quoted field. The field mapping is: `record_id` -> `id`, `age` -> `epoch`, `description` -> `event`, `num` -> `value`, `symbol` -> `glyph`.

### Hint Level 3
For the fixed-width file, use the CSV data to cross-reference: the ID column is 4 characters wide starting at position 0, EPOCH is 12 characters starting at position 4, EVENT is 35 characters starting at position 16, VALUE is 5 characters (right-aligned) starting at position 51, GLYPH is 8 characters starting at position 56.

### Hint Level 4
The XML comments contain fake records (R000 and R006) and a misleading total count of 7. Ignore all comments. For the base64 file, decode the base64 string, parse the resulting JSON, and note that the `n` field contains the value as a hexadecimal string (e.g., `"0x2a"` = 42 decimal).

## Acceptance Criteria

1. The output JSON contains exactly 5 records with IDs R001 through R005
2. All field values match across all 5 source files (after proper parsing and field mapping)
3. Values are integers, not strings
4. The JSON structure matches the Fragment A schema
5. No duplicate or phantom records from XML comment decoys
