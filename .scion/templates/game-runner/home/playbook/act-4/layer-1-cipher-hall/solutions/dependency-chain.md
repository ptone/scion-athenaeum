# Cipher Hall Dependency Chain

## Chain Specification

| Chamber | Cipher Type | Key/Parameter | Source |
|---------|------------|---------------|--------|
| 1 | Caesar / ROT13 | Shift of 13 | Independent (frequency analysis) |
| 2 | Vigenere | CRYSTAL | plain-1 contains "the word CRYSTAL" |
| 3 | Rail Fence | 3 rails | plain-2 contains "number THREE" |
| 4 | Columnar Transposition | ARCHIVE | plain-3 contains "keyword ARCHIVE" |
| 5 | Playfair (5x5, I/J combined) | SENTINEL | plain-4 contains "the word SENTINEL" |
| 6 | Beaufort | MATHIEU | plain-5 contains "the key is MATHIEU" |

## Plaintext Summary

- **plain-1**: "THE ARCHIVE SPEAKS IN RIDDLES THE KEY TO THE NEXT CHAMBER IS THE WORD CRYSTAL"
- **plain-2**: "CRYSTAL CLEAR THE PATH DESCENDS THE RAILS NUMBER THREE IN THE TRANSPOSITION AHEAD"
- **plain-3**: "THREE RAILS CONQUERED THE COLUMNS AWAIT ARRANGE THEM BY THE KEYWORD ARCHIVE"
- **plain-4**: "THE ARCHIVE OPENS THE PLAYFAIR SQUARE AWAITS USE THE WORD SENTINEL TO DECODE"
- **plain-5**: "THE SENTINEL STANDS GUARD THE FINAL CIPHER IS OLD FRENCH THE KEY IS MATHIEU"
- **plain-6**: "FRAGMENT D LIES IN THE CHAMBER BEYOND THIS GATE THE CANTICLES OF FORM AND VOID AWAIT THOSE WHO PROVED WORTHY"

## Notes

- cipher-1 is confirmed ROT13 (Caesar with shift 13)
- The Beaufort cipher (chamber 6) uses the formula C = (K - P) mod 26 for encryption and P = (K - C) mod 26 for decryption, distinguishing it from standard Vigenere
- plain-6 reveals Fragment D's thematic location, leading into Layer 2 (Data Maze)
