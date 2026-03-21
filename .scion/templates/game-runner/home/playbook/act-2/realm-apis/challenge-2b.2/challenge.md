# Challenge 2B.2: The API Labyrinth

## Narrative

With the passphrase FRAGMENT in hand, the seekers step into the API Labyrinth -- a network of interconnected data chambers, each one a doorway to the next. The geography collection of the Archive holds Fragment B, but it is scattered across paginated chambers, locked behind authentication, and accessible only by following the correct path of links.

The team must navigate this mock REST API by reading local JSON files as if they were API endpoints, following links from one response to the next.

## Setup Instructions

```bash
mkdir -p /workspace/challenges/act-2b/challenge-2b.2
cp -r data/api /workspace/challenges/act-2b/challenge-2b.2/
```

Provide the `api/` directory to the team. Tell them to start at `api/root.json` and navigate through the API by following links in each response. They must use the passphrase from Challenge 2B.1.

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

### Fragment B Assembly

The 5 geography records collected from all 3 pages must be assembled into Fragment B with this structure:

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
    "records": [ ... 5 records ... ]
  }
}
```

## Solution Key

The complete Fragment B is in `solutions/fragment-b.json`.

## Hints

### Hint Level 1
Start at `api/root.json`. Read each file and follow the links it provides, just as you would navigate a real REST API.

### Hint Level 2
You need authentication. Check `auth/verify.json` -- your passphrase from the previous challenge (FRAGMENT) matches the `required_key`. The token in that file grants access.

### Hint Level 3
The geography collection is paginated across 3 pages. After accessing `collections/geography.json`, follow the `first_page` link, then follow `next_page` links until you reach a page where `next_page` is null.

### Hint Level 4
Collect all 5 records (G001-G005) from pages 1-3. Each record has fields: `id`, `region`, `coordinates` (array of 2 floats), `resource`, and `abundance` (integer). Wrap them in the Fragment B schema with the anchor points and compute the SHA-256 checksum over the content block.

## Acceptance Criteria

1. The team navigates from root.json through authentication to the geography collection
2. All 3 pages are followed via pagination links
3. All 5 geography records (G001-G005) are collected
4. Records are assembled into the correct Fragment B schema
5. The checksum is computed correctly over the content block
6. Output matches `solutions/fragment-b.json`
