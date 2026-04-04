// feature: char8_t_lang
// macro: __cpp_char8_t
// standard: cpp20
// category: language
// description: char8_t type

auto main() -> int { char8_t c = u8'A'; return c == u8'A' ? 0 : 1; }
