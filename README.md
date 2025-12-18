# Fonetizer

A tool that converts English song lyrics into singing-phonetic tables for vocal performance, optimized for vowel carrying, legato, and minimal consonant friction.

## Purpose

Fonetizer takes English song lyrics (one phrase per line with measure markers) and generates a phonetic table where each phrase is represented by **one column pair**:
- **Left column** = consonant(s), right-aligned
- **Right column** = vowel, left-aligned

These two columns are always read together for singing purposes.

## Installation

Requires Python 3.11+ and dependencies.

```bash
# Clone or download this repository
cd Fonetizer

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Option 1: Web App (Recommended for mobile) 📱

**Streamlit Web Interface:**

Run locally:
```bash
streamlit run app.py
```

Or deploy to Streamlit Cloud for mobile access! See [DEPLOY.md](DEPLOY.md) for instructions.

**Features:**
- 🎵 Mobile-friendly interface
- ✏️ Paste and edit text directly
- 📝 Add line breaks and measure numbers
- 📥 Download formatted Excel file
- 🌐 Share with your quartet via link!

---

### Option 2: Command Line (Desktop)

**Generate formatted Excel file:**
```bash
python fonetizer.py input.txt output.xlsx
```

This creates a fully formatted Excel file with:
- ✅ Borders around column pairs
- ✅ Right-aligned consonants
- ✅ Left-aligned, **bold** vowels
- ✅ Auto-adjusted column widths

**Just open the .xlsx file - no manual formatting needed!**

**Generate CSV file:**
```bash
# To file
python fonetizer.py input.txt output.csv

# To stdout
python fonetizer.py input.txt

# From stdin
cat lyrics.txt | python fonetizer.py
```

CSV files need manual formatting in Excel/Sheets.

## Input Format

Each line must contain:
```
N <text>
```

Where:
- `N` = starting measure number (just the number, no "T" prefix)
- Space (not colon) after the number
- `<text>` = the lyric phrase

**Example:**
```
1 I used to be the first one to cry
4 when I'd think what tomorrow would bring
8 Then you came my way
10 turned my night into day, know
```

**Important:**
- Exactly one phrase per line
- Only starting measure needed (no end measure)
- Do not change phrase divisions

## Output Format

The output is a transposed table in CSV/TSV format:

- **Rows** = syllable positions (1, 2, 3...)
- **Columns** = phrase column pairs (consonant + vowel per phrase)

**Column headers** show measure intervals (T1, T4, etc.)

**Example structure:**
```
Syllable    T1      T4      T4      T8      T8      T10
1           aɪ      j       w       ɛ       ð       ɛ
2           j       uː      d       n       ɛ       n
...
```

Each phrase gets **two columns**:
1. Consonant cluster (right-aligned)
2. Vowel (left-aligned)

## Phonetic Rules

### Syllable Division
Each syllable is split as:
```
[CONSONANT CLUSTER] [VOWEL]
```

- Non-phrase-final consonants move to the next syllable
- Phrase-final consonants stay with their syllable

### Diphthongs
All diphthongs are divided into two separate rows:
```
[Vː | glide]
```

**Examples:**
- `cry` → aː (row 1) + ɪ (row 2)
- `know` → oː (row 1) + ʊ (row 2)
- `way` → eː (row 1) + ɪ (row 2)

The second row (glide) has an **empty consonant column**.

### Specific Pronunciations
- `to` → always `uː`
- `to-` in "tomorrow" → `uː`

## Current Status

✅ **Fully Functional!** The current version implements:
- Full IPA phonetic transcription using the `eng-to-ipa` library
- Proper diphthong splitting into two rows
- Consonant cluster handling
- English-specific pronunciation rules from a comprehensive dictionary

The tool is ready for use with English song lyrics!

## Possible Improvements

Future enhancements could include:
1. Fine-tuning syllable boundary detection
2. Adding support for singing-specific pronunciation variants
3. Handling multi-word phrases more intelligently
4. Export directly to Excel with formatting (bold vowels, cell borders)
5. Web interface for easier use

## Example

Input:
```
T1-T4: I used to be the first one to cry
```

Expected output (when fully implemented):
```
Syllable    T1    T4
1           aɪ    j
2                 ɪ
3           j     uː
4           ...   ...
```

## Contributing

This is a work in progress. The phonetic rules need to be fully implemented based on the specifications in `CLAUDE.md`.

## License

Open source - use freely for vocal training and music education.
