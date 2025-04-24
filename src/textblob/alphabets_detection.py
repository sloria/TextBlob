from enum import Enum

from textblob.utils import unicode_range

latin = (
    unicode_range(0x0041, 0x005A)
    + unicode_range(0x0061, 0x007A)
    + unicode_range(0x00C0, 0x00FF)
    + unicode_range(0x0100, 0x017F)
)
cyrillic = (
    unicode_range(0x0400, 0x04FF)
    + unicode_range(0x0500, 0x052F)
    + unicode_range(0x2DE0, 0x2DFF)
    + unicode_range(0xA640, 0xA69F)
)
arabic = (
    unicode_range(0x0600, 0x06FF)
    + unicode_range(0x0750, 0x077F)
    + unicode_range(0xFB50, 0xFDFF)
    + unicode_range(0xFE70, 0xFEFF)
)
hebrew = unicode_range(0x0590, 0x05FF)
hangul = unicode_range(0xAC00, 0xD7AF) + unicode_range(0x1100, 0x11FF)
georgian = unicode_range(0x10A0, 0x10FF)
ethiopic = unicode_range(0x1200, 0x137F)
thaana = unicode_range(0x0780, 0x07BF)
nko = unicode_range(0x07C0, 0x07FF)
tifinagh = unicode_range(0x2D30, 0x2D7F)
osmanya = unicode_range(0x10480, 0x104AF)
mongolian = unicode_range(0x1800, 0x18AF)
ol_chiki = unicode_range(0x1C50, 0x1C7F)
armenian = unicode_range(0x0530, 0x058F)
devanagari = unicode_range(0x0900, 0x097F)
bengali = unicode_range(0x0980, 0x09FF)
gurmukhi = unicode_range(0x0A00, 0x0A7F)
tamil = unicode_range(0x0B80, 0x0BFF)
telugu = unicode_range(0x0C00, 0x0C7F)
gujarati = unicode_range(0x0A80, 0x0AFF)
kannada = unicode_range(0x0C80, 0x0CFF)
malayalam = unicode_range(0x0D00, 0x0D7F)
sinhala = unicode_range(0x0D80, 0x0DFF)
thai = unicode_range(0x0E00, 0x0E7F)
lao = unicode_range(0x0E80, 0x0EFF)
myanmar = unicode_range(0x1000, 0x109F)
khmer = unicode_range(0x1780, 0x17FF)


class Alphabet(Enum):
    STRING_CONTAINS_NOT_IMPLEMENTED_ALPHABET = 0
    LATIN = 1
    CYRILLIC = 2
    ARABIC = 3
    HEBREW = 4
    HANGUL = 5
    GEORGIAN = 6
    ETHIOPIC = 7
    THAANA = 8
    NKO = 9
    TIFINAGH = 10
    OSMANYA = 11
    MONGOLIAN = 12
    OL_CHIKI = 13
    ARMENIAN = 14
    DEVANAGARI = 15
    BENGALI = 16
    GURMUKHI = 17
    TAMIL = 18
    TELUGU = 19
    GUJARATI = 20
    KANNADA = 21
    MALAYALAM = 22
    SINHALA = 23
    THAI = 24
    LAO = 25
    MYANMAR = 26
    KHMER = 27


alphabets = {
    Alphabet.LATIN: latin,
    Alphabet.CYRILLIC: cyrillic,
    Alphabet.ARABIC: arabic,
    Alphabet.HEBREW: hebrew,
    Alphabet.HANGUL: hangul,
    Alphabet.GEORGIAN: georgian,
    Alphabet.ETHIOPIC: ethiopic,
    Alphabet.THAANA: thaana,
    Alphabet.NKO: nko,
    Alphabet.TIFINAGH: tifinagh,
    Alphabet.OSMANYA: osmanya,
    Alphabet.MONGOLIAN: mongolian,
    Alphabet.OL_CHIKI: ol_chiki,
    Alphabet.ARMENIAN: armenian,
    Alphabet.DEVANAGARI: devanagari,
    Alphabet.BENGALI: bengali,
    Alphabet.GURMUKHI: gurmukhi,
    Alphabet.TAMIL: tamil,
    Alphabet.TELUGU: telugu,
    Alphabet.GUJARATI: gujarati,
    Alphabet.KANNADA: kannada,
    Alphabet.MALAYALAM: malayalam,
    Alphabet.SINHALA: sinhala,
    Alphabet.THAI: thai,
    Alphabet.LAO: lao,
    Alphabet.MYANMAR: myanmar,
    Alphabet.KHMER: khmer,
}


def detect_alphabets(text: str):
    """Detects the percentage of character containing in a string `text` and
    return list with tuples. Tuple contains (Alphabet.name, % of the alphabet
    in the `text`). Any additional languages should be added at top of the file
    as unicode ranges and appended to  the `alphabets` map and `Alphabet` enum.
    """
    only_chars = [x for x in text if x.isalpha()]
    result = []
    progress = 0

    for alphabet_key, alphabet_value in alphabets.items():
        found_chars_sum = sum(1 for x in only_chars if x in alphabet_value)

        percentage = found_chars_sum / len(only_chars) * 100
        progress += percentage

        if percentage > 0:
            result.append((alphabet_key.name, round(percentage, 2)))

        if progress >= 99.99:
            return result

    final_result.append((Alphabet.STRING_CONTAINS_NOT_IMPLEMENTED_ALPHABET.name, 0))
    return result
