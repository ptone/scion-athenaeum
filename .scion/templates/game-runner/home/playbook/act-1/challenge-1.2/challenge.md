# Challenge 1.2 - The Gateway Cipher

## Narrative

*The decoded summons spoke of a Gateway - and here it stands before you, humming with energy. A crystalline arch pulses with light, its surface etched with an intricate web of nodes and pathways. At its base, a terminal displays a JSON data structure: the Map of Connections.*

*But something is wrong. Some of the pathways shimmer and flicker, as if they exist only partially - echoes of routes that were never truly forged. The Gateway demands proof of passage: you must find the true shortest path through the map, from ORIGIN to TERMINUS, and compute the sacred verification code from the values you encounter along the way.*

*Only the correct code will open the Gateway.*

**Objective:** Parse the file `gateway-data.json`, identify the shortest weighted path from the node named "ORIGIN" to the node named "TERMINUS" (ignoring illusory connections), and compute the XOR of all node values along that path (including both ORIGIN and TERMINUS).

## Setup Instructions

Copy the challenge data to the player's workspace:

```bash
cp /path/to/playbook/act-1/challenge-1.2/data/gateway-data.json /workspace/challenges/act-1/gateway-data.json
```

Tell the player: *"The Gateway's Map of Connections has been loaded to `/workspace/challenges/act-1/gateway-data.json`. Find the true shortest path from ORIGIN to TERMINUS and compute the verification code."*

## Data Format

The JSON file has a nested structure:

```
gateway-data.json
  .map_id          -> string
  .version         -> string
  .metadata        -> object (flavor text)
  .nodes[]         -> array of node objects
    .name          -> string (node identifier)
    .properties
      .value       -> integer (used for XOR computation)
      .type        -> "terminal" or "waypoint"
    .connections[] -> array of connection objects
      .target      -> string (target node name)
      .properties
        .weight    -> integer (edge weight for shortest path)
        .metadata
          .verified -> boolean
          .illusory -> boolean (TRUE = fake edge, must be ignored)
```

The graph contains 30 nodes and a mix of real and illusory edges. There are 7 illusory edges that, if followed, would produce shorter-looking paths that are not valid.

## Solution Key

### Correct Shortest Path (by total edge weight)

```
ORIGIN -> Crystal-Nexus -> Rune-Well -> Storm-Alcove -> Gilt-Threshold -> Ashen-Stair -> TERMINUS
```

Total path weight: **13** (edges: 2 + 3 + 2 + 3 + 2 + 1)

### Node Values Along Path

| Node | Value |
|------|-------|
| ORIGIN | 164 |
| Crystal-Nexus | 29 |
| Rune-Well | 36 |
| Storm-Alcove | 140 |
| Gilt-Threshold | 109 |
| Ashen-Stair | 167 |
| TERMINUS | 180 |

### XOR Computation

164 ^ 29 ^ 36 ^ 140 ^ 109 ^ 167 ^ 180 = **111**

### Expected Outputs

- **gateway-answer.txt**: `111`
- **gateway-path.txt**:
  ```
  ORIGIN
  Crystal-Nexus
  Rune-Well
  Storm-Alcove
  Gilt-Threshold
  Ashen-Stair
  TERMINUS
  ```

## Hints (Escalating)

Deliver these one at a time, in order, only when the player is stuck:

1. *"Not all connections are what they seem - look deeper into the metadata of each connection."*
2. *"The 'illusory' field in connection metadata marks phantom connections that must be filtered out before pathfinding."*
3. *"Use Dijkstra's algorithm or BFS on the graph after filtering out all edges where `illusory` is `true`. The edge weights matter - find the minimum total weight path."*

## Acceptance Criteria

Both of the following must be correct:

- [ ] The XOR value matches exactly: **111**
- [ ] The path matches exactly (in order): ORIGIN, Crystal-Nexus, Rune-Well, Storm-Alcove, Gilt-Threshold, Ashen-Stair, TERMINUS

Partial credit: If the player identifies the correct path but computes the wrong XOR value (or vice versa), acknowledge the correct part and guide them to fix the other.

## On Success

Deliver the following:

*"The Gateway flares to life. The crystalline arch blazes with light as your verification code resonates through its structure. The path you traced - ORIGIN through Crystal-Nexus, Rune-Well, Storm-Alcove, Gilt-Threshold, and Ashen-Stair to TERMINUS - was the one true route through the Map of Connections. The Gateway opens, revealing a passage deeper into the Athenaeum. The first fragment of the Codex Machina awaits beyond... but the path ahead will demand even greater skill."*

Then proceed to **Act 2** (when available).
