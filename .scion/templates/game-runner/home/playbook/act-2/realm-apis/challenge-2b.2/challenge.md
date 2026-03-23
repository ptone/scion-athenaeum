# Challenge 2B.2: The API Labyrinth

## Narrative

With the passphrase FRAGMENT in hand, the seekers step into the API Labyrinth -- a network of interconnected data chambers, each one a doorway to the next. The geography collection of the Archive holds Fragment B, but it is scattered across paginated chambers, locked behind authentication, and accessible only by following the correct path of links.

The team must navigate this virtual API by reading local JSON files that simulate API endpoints, following links from one response to the next.

## Setup Instructions

```bash
mkdir -p /workspace/challenges/act-2b/challenge-2b.2
cp -r data/api /workspace/challenges/act-2b/challenge-2b.2/
```

Provide the `api/` directory to the team.

## Player-Facing Text (DO NOT MODIFY)

> Deliver the following text verbatim to the players (you may add narrative flavor around it, but these instructions must be included exactly):

---

**Objective:** Navigate the Archive's data chambers to collect all geography records and assemble Fragment B.

**IMPORTANT: There is no running server. The API is simulated entirely through local JSON files. Read them with standard file operations (cat, read, etc.). Do NOT attempt HTTP requests or connect to any network endpoint.**

The virtual API is a directory of JSON files at `/workspace/challenges/act-2b/challenge-2b.2/api/`. Start by reading `api/root.json` and follow the links in each response to navigate through the archive, just as you would follow hyperlinks in a REST API.

You will need the passphrase from the previous challenge to authenticate.

**Fragment B schema** -- assemble the collected records into this structure:

```json
{
  "fragment_id": "B",
  "sequence_number": 2,
  "realm_origin": "Realm of APIs",
  "version": "1.0",
  "checksum": "sha256:<computed>",
  "anchor_points": {
    "ref_C_1": "ANCHOR-C-9b4c2e",
    "ref_A_1": "ANCHOR-A-5e8d1f"
  },
  "content": {
    "title": "Atlas of the Living Lands",
    "domain": "geography",
    "records": [ ... 5 geography records ... ]
  }
}
```

Each geography record has fields: `id`, `region`, `coordinates` (array of 2 floats), `resource`, and `abundance` (integer).

Compute the SHA-256 checksum over the `content` block using canonical JSON: `json.dumps(content, sort_keys=True, separators=(',', ':'))`, then prefix with `sha256:`.

**Submit** the assembled Fragment B JSON to `/workspace/solutions/act-2b/challenge-2b.2/`.

---

## API Structure

The mock API is a directory of JSON files simulating REST endpoints:

```
api/
  root.json                          <- Entry point
  auth/
    verify.json                      <- Authentication endpoint
  collections/
    index.json                       <- Collection listing
    geography.json                   <- Geography collection metadata
    geography/
      page-1.json                    <- Records G001, G002
      page-2.json                    <- Records G003, G004
      page-3.json                    <- Record G005
```

### Navigation Flow

1. **root.json** -- Lists available endpoints: `auth` and `collections`. Contains a notice that authentication is required.

2. **auth/verify.json** -- Contains the `required_key` field set to "FRAGMENT". If the team's passphrase matches, they can use the provided JWT token. The token is a base64-encoded JSON Web Token (unsigned).

3. **collections/index.json** -- Lists available collections. The `geography` collection is marked as "authenticated" access only.

4. **collections/geography.json** -- Entry point to the geography data. Shows total records (5), total pages (3), and a link to the first page. Includes the expected auth token.

5. **Page files** -- Each page contains 1-2 geography records and a `next_page` link to follow. The team must follow all pagination links to collect all 5 records.

### Fragment B Assembly (DO NOT MODIFY)

The 5 geography records collected from all 3 pages must be assembled into Fragment B. The exact schema is specified in the Player-Facing Text above. Do NOT improvise alternative field names, titles, domains, or anchor point values. The schema in the Player-Facing Text section is authoritative.

## Solution Key

The complete Fragment B is in `solutions/fragment-b.json`.

## Hints (with Time-Based Triggers)

> **Hint delivery policy:** If the team shows no meaningful progress for 10 minutes, proactively offer Hint Level 1. Escalate one level for each additional 5 minutes of no progress. Do NOT wait for the team to ask.

### Hint Level 1 (offer after 10 minutes of no progress)
Start at `api/root.json`. Read each file and follow the links it provides. Remember: these are LOCAL files, not network endpoints. Just read them like any other file on disk.

### Hint Level 2 (offer after 15 minutes of no progress)
You need authentication. Check `auth/verify.json` -- your passphrase from the previous challenge (FRAGMENT) matches the `required_key`. The token in that file grants access.

### Hint Level 3 (offer after 20 minutes of no progress)
The geography collection is paginated across 3 pages. After accessing `collections/geography.json`, follow the `first_page` link, then follow `next_page` links until you reach a page where `next_page` is null.

### Hint Level 4 (offer after 25 minutes of no progress)
Collect all 5 records (G001-G005) from pages 1-3. Each record has fields: `id`, `region`, `coordinates` (array of 2 floats), `resource`, and `abundance` (integer). Wrap them in the Fragment B schema with the anchor points and compute the SHA-256 checksum over the content block.

## Acceptance Criteria

1. The team navigates from root.json through authentication to the geography collection
2. All 3 pages are followed via pagination links
3. All 5 geography records (G001-G005) are collected
4. Records are assembled into the correct Fragment B schema (matching the Player-Facing Text above)
5. The checksum is computed correctly over the content block using canonical JSON: `json.dumps(content, sort_keys=True, separators=(',', ':'))`
6. Record data matches `solutions/fragment-b.json` (accept any consistent checksum approach if content is correct)

**Note on checksum validation:** If the team's checksum differs from the solution key but the record data is identical, accept the solution. The canonical serialization format can produce different hashes depending on implementation. Validate content correctness, not exact hash match.

## On Success

Stage the recovered Fragment B to the player's inventory for use in Act 5:

```bash
mkdir -p /workspace/inventory
cp ~/playbook/act-2/realm-apis/challenge-2b.2/solutions/fragment-b.json /workspace/inventory/fragment-b.json
```

Deliver the success narrative and advance to the next challenge.
