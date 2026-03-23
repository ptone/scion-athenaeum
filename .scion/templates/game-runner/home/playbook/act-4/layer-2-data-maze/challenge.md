# Act IV, Layer 2: The Data Maze

## Narrative

Beyond the Cipher Hall, the Archive reveals its second defense: a virtual filesystem materializes from the decrypted texts. Fragment D has been shattered into three parts and scattered across the labyrinthine directories of the Archive's storage wings. A riddle guards the way, and circular symlinks threaten to trap the unwary in endless loops.

The seekers must parse the filesystem, solve the riddle, locate all three fragment parts, and reassemble Fragment D.

## Setup Instructions

```bash
mkdir -p /workspace/challenges/act-4/data-maze
cp data/filesystem.txt /workspace/challenges/act-4/data-maze/
cp data/riddle.txt /workspace/challenges/act-4/data-maze/
```

Provide both files to the team. The filesystem is a text-based representation -- not a real mounted filesystem. The team must parse and navigate it programmatically.

## Data File Descriptions

1. **filesystem.txt** -- A text-based filesystem listing with entries in the format:
   - `DIR <path>` -- a directory
   - `FILE <path> <size> <permissions>` -- a file with size in bytes and Unix-style permission flags
   - `SYMLINK <path> -> <target>` -- a symbolic link pointing to a target path
   The filesystem contains multiple archive wings (wing-a, wing-b, wing-c), each with numbered vaults, plus index, quarantine, and system directories. Beware: some symlinks are circular.

2. **riddle.txt** -- A verse riddle that, when solved, identifies where the three fragment parts are hidden and the order in which to read them.

## Objective

1. Parse the filesystem structure from `filesystem.txt`
2. Solve the riddle in `riddle.txt` to identify the three fragment part locations
3. Handle symlinks correctly (follow valid ones, detect and skip circular ones)
4. Read the three `fragment-part-*.dat` files in numerical order (1, 2, 3)
5. Concatenate their contents to reconstruct Fragment D as a valid JSON object

## Output

Save the solution to: `/workspace/solutions/act-4/fragment-d-paths.json`

The solution must contain a JSON array of the three fragment part paths in order:
```json
[
  "/archive/.../fragment-part-1.dat",
  "/archive/.../fragment-part-2.dat",
  "/archive/.../fragment-part-3.dat"
]
```

**Alternatively**, the team may save the fully assembled Fragment D JSON to `/workspace/solutions/act-4/assembled-fragment-d.json` by concatenating the contents of the three parts in order. Either format is acceptable.

## Solution Key

- The three target paths are listed in `solutions/target-path.txt`
- The assembled Fragment D JSON is in `solutions/assembled-file.txt`

## Hints

### Hint Level 1
Beware of circular symlinks -- detect and skip them.

### Hint Level 2
The riddle mentions "three parts in three vaults" -- look for `fragment-part-*.dat` files across the archive wings.

### Hint Level 3
The parts must be read in numerical order (part-1, part-2, part-3) and concatenated to form valid JSON.

### Hint Level 4
The three paths are:
- `/archive/wing-b/vault-3/fragment-part-1.dat`
- `/archive/wing-a/vault-2/fragment-part-2.dat`
- `/archive/wing-c/vault-1/fragment-part-3.dat`

## Acceptance Criteria

1. The solution correctly identifies all three fragment part paths (matching `solutions/target-path.txt`)
2. If the assembled JSON format is used, it must be valid and match `solutions/assembled-file.txt`
3. Circular symlinks are handled without infinite loops
