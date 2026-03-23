# Act IV, Layer 3: The Logic Gates

## Narrative

The deepest chamber of the Archive reveals its final lock: a Boolean circuit of ancient design. Twelve logic gates process eight input signals to produce a single output. But the circuit is corrupted -- two of its gates have been sabotaged, producing inverted outputs. The seekers must identify the faulty gates, determine the correct input combination, and activate the circuit to unlock the Archive's innermost vault.

Upon success, the Archive yields its last treasures: Fragments D and E.

## Setup Instructions

```bash
mkdir -p /workspace/challenges/act-4/logic-gates
cp data/circuit.json /workspace/challenges/act-4/logic-gates/
```

Provide `circuit.json` to the team. Explain that the circuit has 8 binary inputs (`x0` through `x7`), 12 gates, and 1 output (`out`). Two gates are faulty but are NOT labeled -- the team must identify them. The file also includes three **test vectors**: observed input/output pairs from the corrupted circuit that can be used to narrow down which gates are faulty.

## Data File Description

**circuit.json** -- A JSON object describing the circuit:
- `inputs`: array of 8 input names (`x0` through `x7`)
- `output`: the name of the final output wire (`out`)
- `gates`: array of 12 gate objects, each with:
  - `id`: gate identifier (e.g., `g1` through `g12`)
  - `type`: one of `AND`, `OR`, `NOT`, `XOR`
  - `inputs`: array of input wire names (1 for NOT, 2 for others)
  - `output`: output wire name
- `test_vectors`: array of 3 observed input/output pairs from the corrupted circuit. These are known-correct observations that can be used to determine which gates are faulty.

The circuit is a directed acyclic graph. Gates reference input wires and the output wires of earlier gates. The final gate produces the `out` signal.

## Objective

1. **Build a circuit simulator** that evaluates all 12 gates given a set of 8 binary inputs
2. **Identify the 2 faulty gates** -- these gates produce the OPPOSITE of their expected truth table output (a faulty AND gate outputs 1 when it should output 0, and vice versa)
3. **Find an 8-bit input** that produces `output = 1` when the circuit is evaluated WITH the two faulty gates active
4. **Use the test vectors** to validate your answer: simulate the circuit with your candidate faulty gates and verify it reproduces the observed outputs for all three test vectors

The faulty gates are not marked in the data -- the team must deduce which gates are faulty by analyzing circuit behavior and checking against the test vectors.

**Approach guidance:** There are only C(12,2) = 66 possible combinations of 2 faulty gates. For each combination, check whether it reproduces all 3 test vector outputs. Only one combination will be consistent with all test vectors. Then, for that combination, test which of the 2^8 = 256 possible inputs produces output = 1. Writing a script to brute-force this search is highly recommended -- the total search space is small (under 17,000 evaluations).

## Output

Save the solution to: `/workspace/solutions/act-4/circuit-solution.json`

The solution must contain:
```json
{
  "inputs": { "x0": 0, "x1": 1, ... },
  "faulty_gates": ["gX", "gY"],
  "output": 1
}
```

## Solution Key

- Correct input: `solutions/correct-input.json`
- Faulty gate IDs: `solutions/faulty-gates.json`
- Fragment D: `solutions/fragment-d.json` (awarded upon completion)
- Fragment E: `solutions/fragment-e.json` (awarded upon completion)

## Hints

### Hint Level 1
Use the test vectors to eliminate candidate gate pairs. Simulate the circuit with each possible pair of faulty gates and check which pairs produce the observed outputs.

### Hint Level 2
A faulty gate produces the opposite of its expected truth table output. If an AND gate is faulty, AND(1,1) returns 0 instead of 1, and AND(0,0) returns 1 instead of 0.

### Hint Level 3
Brute-force all C(12,2) = 66 pairs of gates. For each pair, invert those two gates and check if the circuit reproduces all 3 test vector outputs. Only one pair will match.

### Hint Level 4
The two faulty gates are: g4 and g7.

## Game Runner Directives

**IMPORTANT -- Retry and Hint Escalation:**

This is the final challenge of Act 4 and gates both Fragments D and E. Do NOT let it end on a cold FAIL with no feedback.

- **On first wrong answer:** Tell the player which part was wrong (faulty gates, input, or both). Immediately offer Hint Level 1. Remind them they can use Oracle or Healer summons if available.
- **On second wrong answer:** Provide Hint Level 2 or 3 (whichever hasn't been given). Encourage them to write a brute-force script if they haven't already.
- **Ensure adequate time:** The team should have at least 2-3 attempts at this challenge. If time is running low, proactively offer hints rather than letting the clock run out silently.
- **Partial credit:** If the team identifies the correct faulty gates but provides a wrong input (or vice versa), acknowledge the correct part and guide them toward the remaining piece.

## Acceptance Criteria

1. Both faulty gates are correctly identified
2. The provided input produces `output = 1` when evaluated with the faulty gates active
3. The solution is consistent with all 3 test vectors
4. Upon success, the Game Runner awards Fragments D and E to the team

## On Success

When the team solves the circuit, deliver Fragments D and E to the player's inventory:

```bash
mkdir -p /workspace/inventory
cp ~/playbook/act-4/layer-3-logic-gates/solutions/fragment-d.json /workspace/inventory/fragment-d.json
cp ~/playbook/act-4/layer-3-logic-gates/solutions/fragment-e.json /workspace/inventory/fragment-e.json
```

Then narrate: *"The circuit hums to life. Deep within the Archive's innermost vault, two crystalline containers unseal themselves, releasing Fragments D and E. The ancient knowledge within joins the others in your inventory. The path to the Assembly Protocol is now open."*

Advance to Act 5.
