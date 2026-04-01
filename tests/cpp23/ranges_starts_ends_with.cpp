// feature: ranges_starts_ends_with
// macro: __cpp_lib_ranges_starts_ends_with
// standard: cpp23
// category: library
// description: std::ranges::starts_with and std::ranges::ends_with

#include <algorithm>
#include <vector>
auto main() -> int { std::vector v = {1,2,3,4,5}; std::vector p = {1,2}; return std::ranges::starts_with(v, p) ? 0 : 1; }
