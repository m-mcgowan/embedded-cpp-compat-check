// feature: ranges_contains
// macro: __cpp_lib_ranges_contains
// standard: cpp23
// category: library
// description: std::ranges::contains

#include <algorithm>
#include <vector>
auto main() -> int { std::vector v = {1,2,3}; return std::ranges::contains(v, 2) ? 0 : 1; }
