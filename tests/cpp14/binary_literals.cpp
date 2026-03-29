// feature: binary_literals
// macro: __cpp_binary_literals
// standard: cpp14
// category: language
// description: Binary literals (0b prefix)

auto main() -> int {
    int mask = 0b11001010;
    return (mask & 0xFF) == 0xCA ? 0 : 1;
}
