# Challenge 2B.1: The Information Hunt

## Narrative

The entrance to the Realm of APIs is sealed behind the Archive Index -- a vast wall of seemingly random symbols stretching hundreds of characters across. Somewhere within this wall, a passphrase is hidden. To extract it, the seekers must answer eight questions of knowledge. Each answer yields a number, and each number points to a position in the Archive Index where a single character of the passphrase can be found.

## Setup Instructions

```bash
mkdir -p /workspace/challenges/act-2b/challenge-2b.1
cp data/archive-index.dat /workspace/challenges/act-2b/challenge-2b.1/
cp data/clues.md /workspace/challenges/act-2b/challenge-2b.1/
```

Provide both files to the team. The `clues.md` file contains the 8 research clues. The `archive-index.dat` file is a single line of 500 characters.

**IMPORTANT -- TWO-PHASE DELIVERY:** This challenge (2B.1) MUST be delivered and completed BEFORE Challenge 2B.2. Do NOT merge these into a single challenge description. When the team solves 2B.1, announce success and then deploy 2B.2 as a separate challenge.

## The Clues

Each clue has an unambiguous integer answer. The answer is used as a 0-indexed character position in `archive-index.dat`.

| Clue # | Question | Answer | Position | Character |
|--------|----------|--------|----------|-----------|
| 1 | How many days are in a non-leap year? | 365 | 365 | F |
| 2 | What is the atomic number of gold (Au)? | 79 | 79 | R |
| 3 | What is the ASCII decimal value of the lowercase letter 'a'? | 97 | 97 | A |
| 4 | How many keys are on a standard modern piano? | 88 | 88 | G |
| 5 | How many squares are on a standard chessboard? | 64 | 64 | M |
| 6 | What is the HTTP status code for 'OK'? | 200 | 200 | E |
| 7 | How many degrees are in a right angle? | 90 | 90 | N |
| 8 | The year of the first crewed Moon landing, minus 1900? | 69 | 69 | T |

Reading the characters in clue order spells: **FRAGMENT**

## Solution Key

See `solutions/clue-answers.json` for the complete answer key. The passphrase **FRAGMENT** is needed to access the geography collection in Challenge 2B.2.

## Hints

### Hint Level 1
Each clue answer is a well-known integer. Research each question individually -- the answers are not obscure.

### Hint Level 2
The answers are all common numbers: days in a year, atomic numbers, ASCII codes, etc. Use each answer as a 0-indexed position to read a character from the archive-index.dat file.

### Hint Level 3
Read the characters in order from clue 1 through clue 8 to form the passphrase. The passphrase is a single English word.

### Hint Level 4
The answers are: 365, 79, 97, 88, 64, 200, 90, 69. The characters at these positions spell FRAGMENT.

## Player-Facing Text (DO NOT MODIFY)

> Deliver the following text verbatim to the players:

---

**Objective:** Extract the passphrase hidden in the Archive Index.

You are provided:
1. `archive-index.dat` -- a wall of 500 characters
2. `clues.md` -- 8 research questions

Each clue answer is an integer. Use each answer as a 0-indexed position in `archive-index.dat` to extract one character. Read the 8 extracted characters in clue order to form the passphrase.

**Submit** the passphrase to the Game Runner. You will need it for the next challenge.

---

## Acceptance Criteria

1. All 8 clue answers are correctly identified
2. The correct characters are extracted from archive-index.dat at the answer positions
3. The passphrase FRAGMENT is assembled from the extracted characters
4. The team understands the passphrase will be needed for the next challenge
