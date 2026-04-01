// feature: ranges_iota
// macro: __cpp_lib_ranges_iota
// standard: cpp23
// category: library
// description: std::ranges::iota

#include <numeric>
#include <vector>
auto main() -> int { std::vector<int> v(5); std::ranges::iota(v, 1); return v[0] == 1 && v[4] == 5 ? 0 : 1; }
