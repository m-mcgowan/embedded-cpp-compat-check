// feature: bitops
// macro: __cpp_lib_bitops
// standard: cpp20
// category: library
// description: Bit operations (popcount, etc)
#include <bit>
auto main() -> int {
    return std::popcount(0b1010u) - 2;
}
