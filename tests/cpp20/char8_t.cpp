// feature: char8_t
// macro: __cpp_char8_t
// standard: cpp20
// category: language
// description: char8_t type
auto main() -> int {
    char8_t c = u8'A';
    return static_cast<int>(c) - 65;
}
