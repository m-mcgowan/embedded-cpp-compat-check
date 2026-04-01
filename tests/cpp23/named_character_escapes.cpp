// feature: named_character_escapes
// macro: __cpp_named_character_escapes
// standard: cpp23
// category: language
// description: Named character escapes (e.g. \N{LATIN SMALL LETTER A})

auto main() -> int { char c = '\N{LATIN SMALL LETTER A}'; return c == 'a' ? 0 : 1; }
