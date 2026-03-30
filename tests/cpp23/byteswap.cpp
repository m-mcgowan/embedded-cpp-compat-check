// feature: byteswap
// macro: __cpp_lib_byteswap
// standard: cpp23
// category: library
// description: std::byteswap
#include <bit>
#include <cstdint>
auto main() -> int {
    uint16_t val = 0x0102;
    uint16_t swapped = std::byteswap(val);
    return swapped == 0x0201 ? 0 : 1;
}
