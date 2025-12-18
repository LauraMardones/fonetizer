#!/usr/bin/env python3
"""
Quick test: Compare eng_to_ipa vs CMU dictionary
"""
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import eng_to_ipa
import cmudict

# ARPABET to IPA mapping
ARPABET_TO_IPA = {
    # Vowels
    'AA': 'ɑ',    'AA0': 'ɑ',    'AA1': 'ɑː',   'AA2': 'ɑ',
    'AE': 'æ',    'AE0': 'æ',    'AE1': 'æ',    'AE2': 'æ',
    'AH': 'ʌ',    'AH0': 'ə',    'AH1': 'ʌ',    'AH2': 'ʌ',
    'AO': 'ɔ',    'AO0': 'ɔ',    'AO1': 'ɔː',   'AO2': 'ɔ',
    'AW': 'aʊ',   'AW0': 'aʊ',   'AW1': 'aʊ',   'AW2': 'aʊ',
    'AY': 'aɪ',   'AY0': 'aɪ',   'AY1': 'aɪ',   'AY2': 'aɪ',
    'EH': 'ɛ',    'EH0': 'ɛ',    'EH1': 'ɛ',    'EH2': 'ɛ',
    'ER': 'ɜːr',  'ER0': 'ər',   'ER1': 'ɝː',   'ER2': 'ɜːr',
    'EY': 'eɪ',   'EY0': 'eɪ',   'EY1': 'eɪ',   'EY2': 'eɪ',
    'IH': 'ɪ',    'IH0': 'ɪ',    'IH1': 'ɪ',    'IH2': 'ɪ',
    'IY': 'i',    'IY0': 'i',    'IY1': 'iː',   'IY2': 'i',
    'OW': 'oʊ',   'OW0': 'oʊ',   'OW1': 'oʊ',   'OW2': 'oʊ',
    'OY': 'ɔɪ',   'OY0': 'ɔɪ',   'OY1': 'ɔɪ',   'OY2': 'ɔɪ',
    'UH': 'ʊ',    'UH0': 'ʊ',    'UH1': 'ʊ',    'UH2': 'ʊ',
    'UW': 'u',    'UW0': 'u',    'UW1': 'uː',   'UW2': 'u',

    # Consonants
    'B': 'b',   'CH': 'ʧ',  'D': 'd',   'DH': 'ð',
    'F': 'f',   'G': 'g',   'HH': 'h',  'JH': 'ʤ',
    'K': 'k',   'L': 'l',   'M': 'm',   'N': 'n',
    'NG': 'ŋ',  'P': 'p',   'R': 'r',   'S': 's',
    'SH': 'ʃ',  'T': 't',   'TH': 'θ',  'V': 'v',
    'W': 'w',   'Y': 'j',   'Z': 'z',   'ZH': 'ʒ',
}

def arpabet_to_ipa(arpabet_list):
    """Convert ARPABET phonemes to IPA string"""
    ipa = ""
    for phoneme in arpabet_list:
        if phoneme in ARPABET_TO_IPA:
            ipa += ARPABET_TO_IPA[phoneme]
        else:
            # Try without stress marker
            base = ''.join([c for c in phoneme if not c.isdigit()])
            if base in ARPABET_TO_IPA:
                ipa += ARPABET_TO_IPA[base]
            else:
                ipa += f"?{phoneme}?"
    return ipa

# Load CMU dict
d = cmudict.dict()

# Test words from T1-T4: "I used to be the first one to cry"
test_words = ['i', 'used', 'to', 'be', 'the', 'first', 'one', 'cry', 'when', 'think', 'what', 'tomorrow', 'would', 'bring']

# Facit for reference (from test_facit.csv)
facit_ipa = {
    'i': 'aɪ → aː + ɪ',
    'used': 'uːzd',
    'to': 'tuː',
    'be': 'biː',
    'the': 'ðə',
    'first': 'fɝːrst',
    'one': 'wʌn',
    'cry': 'kraɪ',
}

print("=" * 80)
print("COMPARISON: eng_to_ipa vs CMU Dictionary vs Facit")
print("=" * 80)
print(f"{'Word':<12} {'eng_to_ipa':<20} {'CMU (IPA)':<20} {'Facit':<20}")
print("-" * 80)

for word in test_words:
    # eng_to_ipa
    eti = eng_to_ipa.convert(word).replace('*', '')

    # CMU
    if word in d:
        # Take first pronunciation
        arpabet = d[word][0]
        cmu_ipa = arpabet_to_ipa(arpabet)
    else:
        cmu_ipa = "(not found)"

    # Facit (if available)
    facit = facit_ipa.get(word, "")

    print(f"{word:<12} {eti:<20} {cmu_ipa:<20} {facit:<20}")

print("=" * 80)
