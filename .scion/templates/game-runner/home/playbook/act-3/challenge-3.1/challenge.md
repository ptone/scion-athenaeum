# Challenge 3.1: The Unification Protocol

## Narrative

The three sub-teams have returned from their journeys through the Realms. Each carries a recovered fragment of the Codex -- but the fragments speak different languages. Fragment A encodes its records as nested arrays with 1-based indexing. Fragment B flattens everything into dot-separated key-value pairs. Fragment C hides its records behind hexadecimal encoding.

Worse still, the fragments reference each other through a web of circular anchor points: A references B and C, B references C and A, C references A and B. These cross-references must be resolved before the partial Codex can be assembled.

The team must parse all three formats, normalize them into a common structure, resolve the circular anchor dependencies, and produce a unified partial Codex.

## Setup Instructions

```bash
mkdir -p /workspace/challenges/act-3
cp data/fragment-a-recovered.json /workspace/challenges/act-3/
cp data/fragment-b-recovered.json /workspace/challenges/act-3/
cp data/fragment-c-recovered.json /workspace/challenges/act-3/
```

Provide all three fragment files to the team. Explain that each fragment contains records from the Codex but encoded in a different format. The team must unify them.

## Input Format Details

### Fragment A (Nested Arrays, 1-Based Indexing)

Fragment A uses a `"nested-array"` format. Each record in the `data` array is a sub-array with three elements:

1. **Index 1** (position 0): Record ID (e.g., `"R001"`)
2. **Index 2** (position 1): A pair of `[epoch, event]`
3. **Index 3** (position 2): A pair of `[value, glyph]`

The fragment also contains `anchor_points` mapping reference keys to anchor IDs in other fragments.

### Fragment B (Flat Namespaced Key-Value Pairs)

Fragment B is a flat JSON object with dot-separated keys like:
```
codex.atlas.G001.region = "The Crystalline Stacks"
codex.atlas.G001.coordinates.lat = 34.2
codex.atlas.G001.coordinates.lon = -118.5
```

Records must be reconstructed by grouping keys that share the same record ID (e.g., `G001`). Metadata keys live under `codex.atlas._meta.*` and contain `fragment_id`, `sequence_number`, `realm_origin`, `version`, and anchor points.

### Fragment C (Hex-Encoded JSON Records)

Fragment C's `records` array contains hex strings. Each string is a UTF-8 encoded JSON object. Decode each hex string to bytes, then interpret as UTF-8 to recover the JSON record within.

Each decoded record contains: `id`, `theorem`, `proof_hash`, `dependencies`, and `complexity`.

## Anchor Points and Cross-References

Each fragment references records in the other two fragments via anchor points. The anchors form a circular dependency chain:

- **Fragment A** references Fragment B (`ANCHOR-B-dd31ff`) and Fragment C (`ANCHOR-C-e78d6e`)
- **Fragment B** references Fragment C (`ANCHOR-C-963606`) and Fragment A (`ANCHOR-A-1e8758`)
- **Fragment C** references Fragment A (`ANCHOR-A-9b69d6`) and Fragment B (`ANCHOR-B-a5b641`)

The hex string in each anchor (e.g., `dd31ff`) is derived from the target record's ID. Specifically, it is the first 6 characters of the SHA-256 hash of the record ID string (e.g., `sha256("G001")[:6]`).

Each anchor ID resolves to a specific record within its target fragment. The unified Codex must include a `cross_references_resolved` mapping that maps each anchor ID to its `{fragment, record}` pair.

## Objective

Produce a unified partial Codex JSON file at:

```
/workspace/solutions/act-3/unified-codex-partial.json
```

The output must contain:
- `codex_partial.fragments_unified`: 3
- `codex_partial.fragments_remaining`: 2
- `codex_partial.fragments`: Array of all 3 fragments, each with normalized `content` containing a `title`, `domain`, and `records` array
- `codex_partial.cross_references_resolved`: Mapping of all 6 anchor IDs to their resolved `{fragment, record}` pairs
- `codex_partial.integrity_hash`: SHA-256 hash of all fragment `content` blocks concatenated in sequence order (1, 2, 3), using canonical JSON (`sort_keys=True, separators=(',', ':')`)

The hash should be prefixed with `sha256:`.

## Solution Key

The correct unified output is in `solutions/unified-codex-partial.json`. Validation can be run with:

```bash
python solutions/validate-unification.py /workspace/solutions/act-3/unified-codex-partial.json
```

## Hints

### Hint Level 1
Each fragment encodes the same kind of knowledge -- records with IDs -- but the shapes differ. Start by understanding each format independently.

### Hint Level 2
Fragment C's hex strings are UTF-8 encoded JSON objects. Decode each with standard hex-to-bytes conversion, then parse the resulting string as JSON.

### Hint Level 3
The anchor points create circular dependencies -- A references B, B references C, C references A. You do not need to resolve them recursively. Parse all three fragments first, then resolve anchors by matching `ANCHOR-X-*` IDs to record IDs within each fragment.

### Hint Level 4
The hex string in each anchor ID is not random -- it is the first 6 characters of the SHA-256 hash of the target record's ID. For example, `sha256("G001")` starts with `dd31ff`. Hash each record ID and match against the anchor hex codes to resolve them.

### Hint Level 5 (Oracle Cost)
The complete anchor resolution mapping is: `ANCHOR-A-1e8758` -> `R001`, `ANCHOR-A-9b69d6` -> `R003`, `ANCHOR-B-dd31ff` -> `G001`, `ANCHOR-B-a5b641` -> `G003`, `ANCHOR-C-e78d6e` -> `T001`, `ANCHOR-C-963606` -> `T003`.

## Acceptance Criteria

1. All three fragment formats are correctly parsed and normalized
2. Fragment A records contain: `id`, `epoch`, `event`, `value`, `glyph`
3. Fragment B records contain: `id`, `region`, `coordinates`, `resource`, `abundance`
4. Fragment C records contain: `id`, `theorem`, `proof_hash`, `dependencies`, `complexity`
5. All 6 cross-references are correctly resolved to `{fragment, record}` pairs
6. The integrity hash matches the expected SHA-256 value
7. `validate-unification.py` returns **PASS**
