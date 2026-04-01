// feature: constexpr_numeric
// macro: __cpp_lib_constexpr_numeric
// standard: cpp20
// category: library
// description: constexpr std::accumulate

#include <numeric>
#include <array>
constexpr int f() { std::array<int, 3> a = {1, 2, 3}; return std::accumulate(a.begin(), a.end(), 0); }
static_assert(f() == 6);
auto main() -> int { return 0; }
