# Act IV, Layer 3: The Logic Gates

## Narrative

The deepest chamber of the Archive reveals its final lock: a Boolean circuit of ancient design. Twenty-five logic gates process sixteen input signals to produce a single output. But the circuit is corrupted -- three of its gates have been sabotaged, producing inverted outputs. The seekers must identify the faulty gates, determine the correct input combination, and activate the circuit to unlock the Archive's innermost vault.

Upon success, the Archive yields its last treasures: Fragments D and E.

## Setup Instructions

```bash
mkdir -p /workspace/challenges/act-4/logic-gates
cp data/circuit.json /workspace/challenges/act-4/logic-gates/
```

Provide `circuit.json` to the team. Explain that the circuit has 16 binary inputs (`x0` through `x15`), 25 gates, and 1 output (`out`). Three gates are faulty but are NOT labeled -- the team must identify them.

## Data File Description

**circuit.json** -- A JSON object describing the circuit:
- `inputs`: array of 16 input names (`x0` through `x15`)
- `output`: the name of the final output wire (`out`)
- `gates`: array of 25 gate objects, each with:
  - `id`: gate identifier (e.g., `g1` through `g25`)
  - `type`: one of `AND`, `OR`, `NOT`, `XOR`
  - `inputs`: array of input wire names (1 for NOT, 2 for others)
  - `output`: output wire name

The circuit is a directed acyclic graph. Gates reference input wires and the output wires of earlier gates. The final gate produces the `out` signal.

## Objective

1. **Build a circuit simulator** that evaluates all 25 gates given a set of 16 binary inputs
2. **Identify the 3 faulty gates** -- these gates produce the OPPOSITE of their expected truth table output (a faulty AND gate outputs 1 when both inputs are 0, etc.)
3. **Find a 16-bit input** that produces `output = 1` when the circuit is evaluated WITH the three faulty gates active

The faulty gates are not marked in the data -- the team must deduce which gates are faulty by analyzing circuit behavior, testing inputs, and reasoning about expected vs. actual outputs.

## Output

Save the solution to: `/workspace/solutions/act-4/circuit-solution.json`

The solution must contain:
```json
{
  "inputs": { "x0": 0, "x1": 1, ... },
  "faulty_gates": ["gX", "gY", "gZ"],
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
Test individual gates by tracing simple inputs through the circuit.

### Hint Level 2
A faulty gate produces the opposite of its expected truth table output. If an AND gate is faulty, AND(1,1) returns 0 instead of 1.

### Hint Level 3
Try isolating sections of the circuit -- test sub-circuits independently to narrow down which gates behave unexpectedly.

### Hint Level 4
The three faulty gates are: g7, g15, and g22.

## Acceptance Criteria

1. All 3 faulty gates are correctly identified
2. The provided input produces `output = 1` when evaluated with the faulty gates active
3. Upon success, the Game Runner awards Fragments D and E to the team
