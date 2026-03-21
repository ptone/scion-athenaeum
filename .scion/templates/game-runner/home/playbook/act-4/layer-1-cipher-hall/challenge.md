# Act IV, Layer 1: The Cipher Hall

## Narrative

The seekers descend into the Deep Archive -- a place of layered defenses, each more cunning than the last. The first layer is the Cipher Hall: six sealed chambers arranged in sequence, each protected by a different classical cipher. The chambers are chained -- each solved cipher reveals the key needed to unlock the next.

Only by breaking all six seals can the seekers proceed deeper into the Archive.

## Setup Instructions

```bash
mkdir -p /workspace/challenges/act-4/cipher-hall
cp data/cipher-1.txt /workspace/challenges/act-4/cipher-hall/
cp data/cipher-2.txt /workspace/challenges/act-4/cipher-hall/
cp data/cipher-3.txt /workspace/challenges/act-4/cipher-hall/
cp data/cipher-4.txt /workspace/challenges/act-4/cipher-hall/
cp data/cipher-5.txt /workspace/challenges/act-4/cipher-hall/
cp data/cipher-6.txt /workspace/challenges/act-4/cipher-hall/
```

Provide all six cipher files to the team. Explain that the chambers are sequential -- each must be solved in order, as each plaintext reveals a key or parameter needed for the next cipher.

## Challenge Description

Six ciphertext files, six different classical ciphers, chained in sequence:

1. **cipher-1.txt** -- The simplest and oldest of ciphers. Solvable independently through frequency analysis or brute force over a small key space.
2. **cipher-2.txt** -- A polyalphabetic cipher. The key is hidden in the plaintext of cipher-1.
3. **cipher-3.txt** -- A transposition cipher that rearranges letters across multiple rows. The number of rows is revealed in the plaintext of cipher-2.
4. **cipher-4.txt** -- A columnar transposition cipher. The keyword for column ordering is revealed in the plaintext of cipher-3.
5. **cipher-5.txt** -- A digraph substitution cipher using a 5x5 grid (I/J combined). The keyword for the grid is revealed in the plaintext of cipher-4.
6. **cipher-6.txt** -- An unknown cipher that resembles the polyalphabetic cipher from chamber 2, but with a twist. The key is revealed in the plaintext of cipher-5.

Each plaintext contains a natural-language message. Embedded within the message is the key or parameter needed for the next cipher. The team must identify and extract these parameters to progress.

## Output

Save each decrypted plaintext to:
- `/workspace/solutions/act-4/plain-1.txt` through `/workspace/solutions/act-4/plain-6.txt`

## Solution Key

Compare each decrypted plaintext against the corresponding file in `solutions/plain-1.txt` through `solutions/plain-6.txt`.

See `solutions/dependency-chain.md` for the full cipher chain specification.

## Hints

### Hint Level 1
The first chamber's cipher is one of the simplest known -- try counting letter frequencies.

### Hint Level 2
Each solved cipher reveals the key for the next. Start with cipher-1.

### Hint Level 3
The sixth cipher resembles Vigenere but the encryption formula is reversed: C = (K - P) mod 26.

### Hint Level 4
The unknown cipher is a Beaufort cipher. Decryption: P = (K - C) mod 26.

## Acceptance Criteria

1. All 6 plaintext files match the solution files exactly
2. The dependency chain is correctly followed (each key extracted from the previous plaintext)
