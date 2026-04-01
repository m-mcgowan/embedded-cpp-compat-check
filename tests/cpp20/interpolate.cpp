// feature: interpolate
// macro: __cpp_lib_interpolate
// standard: cpp20
// category: library
// description: std::lerp and std::midpoint

#include <numeric>
auto main() -> int { auto m = std::midpoint(1, 3); auto l = std::lerp(0.0, 1.0, 0.5); return (m == 2 && l == 0.5) ? 0 : 1; }
