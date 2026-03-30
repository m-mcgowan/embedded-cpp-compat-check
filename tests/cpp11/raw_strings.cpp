// feature: raw_strings
// macro: __cpp_raw_strings
// standard: cpp11
// category: language
// description: Raw string literals

auto main() -> int { const char* s = R"(hello)"; return s[0]=='h' ? 0 : 1; }
