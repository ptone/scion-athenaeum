# Challenge 2C.1: The Logic Grid

## Narrative

The Realm of Patterns demands proof of logical reasoning before it will yield its secrets. An 8x8 grid of stone tiles stands at the entrance, some already inscribed with numbers. The seekers must complete the grid by filling every empty cell with a number from 1 to 8, obeying a set of ancient constraints carved into the chamber walls.

Only when the grid is complete and every constraint satisfied will the Pattern Lock in Challenge 2C.2 accept the solution as a key.

## Setup Instructions

```bash
mkdir -p /workspace/challenges/act-2c/challenge-2c.1
cp data/logic-grid.json /workspace/challenges/act-2c/challenge-2c.1/
```

Provide the `logic-grid.json` file to the team. It contains the grid dimensions, the constraint definitions, and the pre-filled cell values.

## The Constraints

The grid is 8x8. Each cell must contain a number from 1 to 8.

| ID | Constraint |
|----|-----------|
| C1 | Each row must contain each number from 1 to 8 exactly once |
| C2 | Each column must contain each number from 1 to 8 exactly once |
| C3 | The sum of values in each row must equal 36 |
| C4 | No two orthogonally adjacent cells (sharing an edge) may contain consecutive numbers (numbers differing by exactly 1) |
| C5 | The four corner cells at positions (0,0), (0,7), (7,0), and (7,7) must sum to exactly 20 |

Note: C3 is automatically satisfied if C1 is satisfied (since 1+2+3+4+5+6+7+8 = 36), but it serves as a useful verification check.

## Grid Format

The `logic-grid.json` file contains:
- `grid_size`: 8
- `value_range`: [1, 8]
- `constraints`: Array of constraint definitions
- `initial_values`: Array of pre-filled cells, each with `row`, `col`, and `value`
- `filled_cells_count`: Number of pre-filled cells
- `empty_cells_count`: Number of cells to solve

The team must output a complete 8x8 grid as a 2D array (list of 8 lists, each containing 8 integers).

## Solution Key

The solved grid is in `solutions/solved-grid.json`.

## Hints

### Hint Level 1
Start with constraints C1 and C2 -- this is a Latin square. Use the pre-filled values to eliminate possibilities for each empty cell.

### Hint Level 2
Constraint C4 is the most restrictive: no two adjacent cells can have consecutive values. After filling in obvious cells from the Latin square constraints, use C4 to eliminate further candidates. For example, if a cell contains 5, no adjacent cell can contain 4 or 6.

### Hint Level 3
The corner constraint C5 can help narrow down corner values early. The four corners must sum to 20. If three corners are known, the fourth is determined.

### Hint Level 4
Use a systematic approach: maintain a candidate set for each empty cell. Iteratively eliminate candidates based on all constraints. When a cell has only one candidate left, fill it in and propagate. If stuck, use backtracking with the most constrained cell first.

## Acceptance Criteria

1. The grid is 8x8 with all cells filled with values 1-8
2. Every row contains each number 1-8 exactly once (C1)
3. Every column contains each number 1-8 exactly once (C2)
4. Each row sums to 36 (C3)
5. No two orthogonally adjacent cells contain consecutive numbers (C4)
6. The four corner cells sum to exactly 20 (C5)
7. All pre-filled values from the puzzle remain unchanged
8. The output matches `solutions/solved-grid.json`
