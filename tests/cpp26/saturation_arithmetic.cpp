// feature: saturation_arithmetic
// macro: __cpp_lib_saturation_arithmetic
// standard: cpp26
// category: library
// description: Saturation arithmetic

#include <numeric>
#include <cstdint>
auto main() -> int { return std::add_sat<uint8_t>(200, 200) == 255 ? 0 : 1; }
