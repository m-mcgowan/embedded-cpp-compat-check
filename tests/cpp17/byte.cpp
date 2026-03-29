// feature: byte
// macro: __cpp_lib_byte
// standard: cpp17
// category: library
// description: std::byte type

#include <cstddef>

auto main() -> int {
    std::byte b{0x42};
    return std::to_integer<int>(b) - 0x42;
}
