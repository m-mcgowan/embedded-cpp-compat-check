// feature: constexpr_algorithms
// macro: __cpp_lib_constexpr_algorithms
// standard: cpp20
// category: library
// description: Constexpr algorithms

#include <algorithm>
#include <array>
constexpr auto f() { std::array a{3,1,2}; std::sort(a.begin(), a.end()); return a[0]; }
static_assert(f() == 1);
auto main() -> int { return 0; }
