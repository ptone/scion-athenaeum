# Challenge 2C.2: The Pattern Lock

## Narrative

The completed logic grid pulses with energy as the seekers place the final tile. Across the chamber, the Pattern Lock awakens -- an ancient mechanism guarding Fragment C. A hexadecimal inscription covers the lock's surface: rows upon rows of encoded data, waiting to be transformed back into meaning.

The grid solution proves the seekers' worthiness. The Pattern Lock recognizes this proof and reveals how to decode the hex inscription into Fragment C -- the final piece of the Athenaeum's second act.

## Setup Instructions

```bash
mkdir -p /workspace/challenges/act-2c/challenge-2c.2
cp data/pattern-data.hex /workspace/challenges/act-2c/challenge-2c.2/
```

Provide the `pattern-data.hex` file to the team. Tell them that the solved grid from Challenge 2C.1 serves as proof of worthiness, and that the hex data can now be decoded.

## The Pattern Lock Mechanism (DO NOT MODIFY)

> The decoding process below must be delivered to players exactly as specified. Do NOT add extra steps (XOR ciphers, filters, sorting, etc.) beyond what is listed here.

The `pattern-data.hex` file contains hex-encoded data. The decoding process is:

1. **Prove worthiness** by solving the logic grid (Challenge 2C.1)
2. **Read the hex data** from `pattern-data.hex`, stripping any whitespace and newlines
3. **Decode the hex string** back into raw bytes
4. **Interpret the bytes** as UTF-8 text
5. **Parse the resulting text** as JSON to obtain Fragment C

The hex encoding is straightforward: each pair of hex characters represents one byte of the original JSON text. The file is split across multiple lines for readability, but the lines should be concatenated before decoding.

There are no additional transformation steps. The decoded JSON IS Fragment C.

## Fragment C Schema (DO NOT MODIFY)

The decoded JSON must match the Fragment C structure:

```json
{
  "fragment_id": "C",
  "sequence_number": 3,
  "realm_origin": "Realm of Patterns",
  "version": "1.0",
  "checksum": "sha256:<computed>",
  "anchor_points": {
    "ref_A_1": "ANCHOR-A-3f7b4c",
    "ref_B_1": "ANCHOR-B-1a6e5d"
  },
  "content": {
    "title": "Theorems of the Eternal Pattern",
    "domain": "mathematics",
    "records": [ ... 5 theorem records ... ]
  }
}
```

Each record has fields: `id`, `theorem`, `proof_hash`, `dependencies` (array of theorem IDs), and `complexity` (integer).

## Solution Key

The complete Fragment C is in `solutions/fragment-c.json`.

## Hints

### Hint Level 1
The hex file contains encoded text. Each pair of hex characters is one byte.

### Hint Level 2
Read all lines from `pattern-data.hex`, join them into a single string (removing newlines), then convert from hex to bytes: `bytes.fromhex(hex_string)`.

### Hint Level 3
The decoded bytes are UTF-8 JSON text. Parse it directly with any JSON parser to get Fragment C.

### Hint Level 4
In Python: `import json; hex_data = open('pattern-data.hex').read().replace('\n',''); fragment_c = json.loads(bytes.fromhex(hex_data).decode('utf-8'))`. The Game Runner will verify both the solved grid AND the decoded fragment.

## Acceptance Criteria

1. The logic grid from Challenge 2C.1 is correctly solved (prerequisite)
2. The hex data is properly decoded from hexadecimal to UTF-8 text
3. The decoded text is valid JSON matching the Fragment C schema
4. All 5 theorem records are present with correct fields
5. The checksum in the fragment is valid (SHA-256 of the content block, using canonical JSON: `json.dumps(content, sort_keys=True, separators=(',', ':'))`)
6. Record data matches `solutions/fragment-c.json` (accept any consistent checksum approach if content is correct)

## On Success

Stage the recovered Fragment C to the player's inventory for use in Act 5:

```bash
mkdir -p /workspace/inventory
cp ~/playbook/act-2/realm-patterns/challenge-2c.2/solutions/fragment-c.json /workspace/inventory/fragment-c.json
```

Deliver the success narrative and advance to the next challenge.
