// feature: gcd_lcm
// macro: __cpp_lib_gcd_lcm
// standard: cpp17
// category: library
// description: std::gcd and std::lcm

#include <numeric>

auto main() -> int {
    return std::gcd(12, 8) - 4;
}
