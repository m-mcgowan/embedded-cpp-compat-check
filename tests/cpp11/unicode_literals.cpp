// feature: unicode_literals
// macro: __cpp_unicode_literals
// standard: cpp11
// category: language
// description: Unicode string literals (u"", U"", u8"")

auto main() -> int { const char16_t* s16 = u"hello"; const char32_t* s32 = U"world"; return (s16[0] == u'h' && s32[0] == U'w') ? 0 : 1; }
