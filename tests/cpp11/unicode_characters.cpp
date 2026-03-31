// feature: unicode_characters
// macro: __cpp_unicode_characters
// standard: cpp11
// category: language
// description: char16_t and char32_t Unicode character types

auto main() -> int { char16_t c16 = u'A'; char32_t c32 = U'A'; return (c16 == u'A' && c32 == U'A') ? 0 : 1; }
