// feature: saturation_arithmetic
// macro: __cpp_lib_saturation_arithmetic
// standard: cpp26
// category: library
// description: Saturation arithmetic

#include <numeric>
auto main() -> int { return std::saturate_cast<unsigned char>(300) == 255 ? 0 : 1; }
