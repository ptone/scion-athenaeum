# Challenge 1.1 - Decode the Summons

## Narrative

*A crackle of static fills the terminal. Line by line, a file materializes in your workspace - dense, unreadable, clearly not meant for casual eyes. The file header bears a cryptic reference string, and the body is a wall of encoded text. Someone - or something - has gone to great lengths to obscure this message.*

*This is no ordinary transmission. The Athenaeum does not reveal its secrets to the unworthy. To read the summons, you must peel back its layers of protection. Only then will the true message - and your quest - be revealed.*

**Objective:** Decode the file `summons.txt` to reveal the plaintext message hidden within. The message has been encoded with multiple layers of obfuscation. Your task is to identify each layer and reverse it.

## Setup Instructions

Copy the challenge data to the player's workspace:

```bash
mkdir -p /workspace/challenges/act-1/
cp /path/to/playbook/act-1/challenge-1.1/data/summons.txt /workspace/challenges/act-1/summons.txt
```

Tell the player: *"A transmission has arrived in your workspace at `/workspace/challenges/act-1/summons.txt`. Decode it."*

## Solution Key

### Encoding Layers (outermost to innermost)

1. **Base64 encoding** - The bulk of the file body is Base64 encoded.
2. **ROT13** - After decoding Base64, the result is ROT13-rotated text.
3. **Keyword substitution cipher** - After reversing ROT13, the text is enciphered with a monoalphabetic substitution cipher using the keyword "KEYWORD".

### The Keyword Discovery

The first line of summons.txt is a comment/reference line:
```
# REF:7f3a-TRANS:4b45-SEQ:5957-CHK:4f52-END:4400
```

The hex pairs embedded in the labeled fields decode to ASCII characters:
- TRANS: `4b` = K, `45` = E
- SEQ: `59` = Y, `57` = W
- CHK: `4f` = O, `52` = R
- END: `44` = D, `00` = null terminator (ignored)

These spell **KEYWORD**, which is the key for the substitution cipher.

### Substitution Cipher Alphabet

Using keyword "KEYWORD" (deduplicated: K, E, Y, W, O, R, D):

| Plaintext  | A | B | C | D | E | F | G | H | I | J | K | L | M | N | O | P | Q | R | S | T | U | V | W | X | Y | Z |
|------------|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Ciphertext | K | E | Y | W | O | R | D | A | B | C | F | G | H | I | J | L | M | N | P | Q | S | T | U | V | X | Z |

### Expected Plaintext

```
Hearken, seekers of lost knowledge. The Codex Machina, ancient repository of the Archive Kingdoms, lies shattered across five realms. Five fragments must be recovered before the Entropy Storm consumes what remains. Seek the Gateway in the data that follows. It opens only to those who can compute the sacred path through the Map of Connections. The coordinates of each fragment shall be revealed to those who prove worthy. Time is not your ally. The storm approaches.
```

### Key Phrases to Verify

- "five fragments"
- "Codex Machina"
- "Gateway"
- "Map of Connections"

## Hints (Escalating)

Deliver these one at a time, in order, only when the player is stuck:

1. *"The outer layer is a common encoding used in email attachments."*
2. *"After removing the first layer, the text appears shifted by a familiar rotation."*
3. *"The comment line at the top isn't random - look for hex-encoded ASCII values in the labeled fields."*
4. *"The hex values spell a keyword for a monoalphabetic substitution cipher."*

## Acceptance Criteria

The player's decoded output must contain ALL of the following phrases (case-insensitive matching is acceptable):

- [ ] "five fragments"
- [ ] "Codex Machina"
- [ ] "Gateway"
- [ ] "Map of Connections"

If all four key phrases are present and the overall message is coherent, the challenge is solved.

## On Success

Deliver the following:

*"The summons is clear. The Codex Machina - the ancient repository of all knowledge in the Archive Kingdoms - has been shattered. Five fragments lie scattered across dangerous realms, and an Entropy Storm threatens to consume them forever. But the message speaks of a Gateway... and a Map of Connections. Perhaps the next file in your workspace holds the key to finding it."*

Then proceed to **Challenge 1.2 - The Gateway Cipher**.
