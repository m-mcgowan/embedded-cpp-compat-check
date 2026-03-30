// feature: ranges_fold
// macro: __cpp_lib_ranges_fold
// standard: cpp23
// category: library
// description: std::ranges::fold_left

#include <algorithm>
#include <numeric>
#include <vector>
auto main() -> int { std::vector v = {1,2,3}; return std::ranges::fold_left(v, 0, std::plus{}) - 6; }
