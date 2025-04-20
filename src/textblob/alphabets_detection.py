from enum import Enum
from string import punctuation, whitespace
from typing import List, Tuple
from unicodedata import category

from textblob.utils import unicode_range

latin = unicode_range(0x0041, 0x005A) + unicode_range(0x0061, 0x007A) + unicode_range(0x00C0, 0x00FF) + unicode_range(
    0x0100, 0x017F)
cyrillic = unicode_range(0x0400, 0x04FF) + unicode_range(0x0500, 0x052F) + unicode_range(0x2DE0,
                                                                                         0x2DFF) + unicode_range(0xA640,
                                                                                                                 0xA69F)
arabic = unicode_range(0x0600, 0x06FF) + unicode_range(0x0750, 0x077F) + unicode_range(0xFB50, 0xFDFF) + unicode_range(
    0xFE70, 0xFEFF)
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


class Alphabet(Enum):
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
    Alphabet.OL_CHIKI: ol_chiki
}

test_string = (
        "Latin: hello; " +
        "Cyrillic: Привет; " +
        "Arabic: مرحبا; " +
        "Hebrew: שלום; " +
        "Hangul: 안녕하세요; " +
        "Georgian: გამარჯობა; " +
        "Ethiopic: ሰላም; " +
        "Thaana: ޝީހް; " +
        "N’Ko: ߣߊ߫; " +
        "Tifinagh: ⴰⵣⵓⵍ; " +
        "Osmanya: 𐒝𐒛𐒒𐒚; " +
        "Mongolian: ᠰᠠᠶᠠᠨ ᠤᠯᠤ; " +
        "Ol Chiki: ᱦᱚᱞᱚ"
)


def alphabets_detection(text: str):
    only_chars = [x for x in text if x.isalpha()]
    alphabets_result = {}
    current_percentage = 0

    for alphabet_key, alphabet_value in alphabets.items():
        chars = sum(1 for x in only_chars if x in alphabet_value)
        is_completed, result, current_percentage = is_current_percentage_completed(chars, current_percentage,
                                                                                   only_chars, alphabet_key,
                                                                                   alphabets_result)
        if is_completed:
            return result

    return None


def is_current_percentage_completed(alphabet_chars_sum: int, current_percent: int, chars: List,
                                    current_language: Alphabet, languages_result: dict) -> Tuple[bool, dict, float]:
    percentage = alphabet_chars_sum / len(chars) * 100
    languages_result[current_language.name] = percentage

    if current_percent + percentage >= 100:
        return True, languages_result, current_percent + percentage

    return False, languages_result, current_percent + percentage
