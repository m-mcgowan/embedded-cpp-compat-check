// feature: bit_cast
// macro: __cpp_lib_bit_cast
// standard: cpp20
// category: library
// description: std::bit_cast

#include <bit>
#include <cstdint>

auto main() -> int {
    float f = 0.0f;
    auto bits = std::bit_cast<uint32_t>(f);
    return bits == 0 ? 0 : 1;
}
