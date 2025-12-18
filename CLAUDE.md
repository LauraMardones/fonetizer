# Fonetizer

> A tool that converts English song lyrics into a singing-phonetic table for vocal performance, optimized for vowel carrying, legato, and minimal consonant friction.

## Purpose

Takes English song lyrics (one phrase per line with measure markers) and generates a phonetic table where each phrase is represented by ONE COLUMN PAIR:
- Left column = consonant(s), right-aligned
- Right column = vowel, left-aligned

These two columns are always read together.

## Tech Stack

- **Language**: Python 3.11+
- **Dependencies**: None (standard library only)
- **Output**: CSV/TSV for Excel/Google Sheets

## Project Structure

```
Fonetizer/
├── fonetizer.py        # Main CLI script
├── example_input.txt   # Example song lyrics
├── CLAUDE.md           # This file
└── README.md           # Usage instructions
```

## Commands

```bash
# Run with file input
python fonetizer.py example_input.txt

# Run with stdin
cat lyrics.txt | python fonetizer.py

# Output to file
python fonetizer.py input.txt > output.csv
```

## Input Format (BINDING)

Each line must contain:
```
N <text>
```

**Rules:**
- `N` is the starting measure number (no "T" prefix)
- Space (not colon) after the number
- Only starting measure needed (no end measure)
- Exactly one phrase per line
- Claude MUST NOT change phrase division

**Example:**
```
1 I used to be the first one to cry
4 when I'd think what tomorrow would bring
8 Then you came my way
10 turned my night into day, know
```

## Output Format (BINDING)

### 1. Table Structure

- Each phrase → TWO columns
- Column A: consonants (right-aligned)
- Column B: vowel (left-aligned)
- Column headers show starting measure on left column only:
  ```
  T1 |
  ```

**Whole table is transposed:**
- Rows = syllable index (1, 2, 3…)
- Columns = phrase column pairs

**Example column headers:**
```
Syllable ↓ | T1 |   | T4 |   | T8 |   | T10 |   | ...
```

(Only the left column of each pair has the measure number)

### 2. Syllable Model (CRITICAL)

Each syllable is divided EXACTLY like this:
```
[CONSONANT CLUSTER]   [VOWEL]
```

**Consonant cluster:**
- Clustered without spaces (ndm, stw, ŋkw)
- Never includes vowels

**Vowel:**
- Exactly one vowel nucleus
- Diphthongs divided according to rules below

**All non-phrase-final consonants move forward to next syllable**

Each syllable occupies one row in the table.

### 3. Phonetic Rules (STRICT)

#### Vowels
- NEVER change the vowel nucleus
- The vowel is the end of the syllable
- Phrase-final consonants may remain (e.g. bring, old)

#### Diphthongs
All diphthongs are divided according to:
```
[Vː | glide]
```

**Examples:**
- cry → aː + ɪ
- know → oː + ʊ
- way → eː + ɪ

The glide is vocalic, NOT [w]/[j].

#### Specific Pronunciations
- `to` → always uː
- `to-` in "tomorrow" → uː

**Distinction between:**
- Consonantal w (what)
- Vocalic ʊ (know)

### 4. Diphthongs – Row Separation (BINDING)

When a diphthong is divided according to:
```
[Vː | glide]
```

It MUST be realized as two separate syllables on two separate rows in the table.

**Rules:**
- **First part (Vː):**
  - Belongs to the syllable where the diphthong begins
  - Written in normal consonant–vowel structure

- **Second part (glide, e.g. ɪ, ʊ):**
  - Placed on its own new row
  - Has NO consonant
  - Written ONLY in the vowel column
  - Consonant column left EMPTY

**Example (principle):**
```
Consonant    Vowel
k            aː
             ɪ
```

This applies to ALL diphthongs without exception.

### 5. Alignment & Typography

- **Consonant column:** right-aligned
- **Vowel column:** left-aligned
- Empty cells left empty
- NO `|` used in output (columns replace this)
- NO comments in output

**(Optional but recommended)**
- Vowel cell can be bold for clarity

### 6. Grouping Marker (Frame)

Claude cannot draw real cell borders, but MUST:
- Consistently maintain two columns per phrase
- NEVER break this pattern
- So that the user can easily add frames around each column pair in Sheets/Docs

### 7. Absolute Constraints

- NO meta-text
- NO explanations
- NO normalization toward "correct English"
- NO common vowel assumptions
- ALL processing happens per complete phrase

## Implementation Notes

### Algorithm Steps
1. Parse input line by line
2. Extract measure markers (Tstart-Tend)
3. Extract phrase text
4. Apply phonetic rules to each phrase:
   - Identify syllables
   - Separate consonant clusters from vowels
   - Handle diphthongs (split into two rows)
   - Move non-final consonants to next syllable
5. Build transposed table structure:
   - Rows = syllable positions
   - Columns = phrase pairs (consonant, vowel)
6. Output as CSV/TSV

### Edge Cases
- Phrase-final consonants stay with their syllable
- Silent letters are removed
- Consonant clusters at syllable boundaries
- Word boundaries within phrases (don't affect syllable division)

## Verification

Before considering work complete:
1. Test with example input
2. Verify diphthongs are split into two rows
3. Check consonant-vowel alignment
4. Confirm measure markers in headers
5. Ensure no meta-text or explanations in output

## File Boundaries

- **Safe to edit**: `fonetizer.py`, `example_input.txt`, `README.md`
- **Never touch**: `.git/`, `__pycache__/`

## Common Tasks

### Testing the Script
```bash
python fonetizer.py example_input.txt
```

### Adding New Phonetic Rules
1. Edit the phonetic rule functions in `fonetizer.py`
2. Test with various inputs
3. Verify output format remains correct

### Debugging
```bash
# Add debug prints to see intermediate steps
python fonetizer.py input.txt --debug
```
