// feature: array_constexpr
// macro: __cpp_lib_array_constexpr
// standard: cpp17
// category: library
// description: Constexpr std::array

#include <array>
constexpr std::array<int,3> a = {1,2,3};
auto main() -> int { return a[0] + a[1] + a[2] - 6; }
