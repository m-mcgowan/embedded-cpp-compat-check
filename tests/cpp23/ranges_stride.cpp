// feature: ranges_stride
// macro: __cpp_lib_ranges_stride
// standard: cpp23
// category: library
// description: std::views::stride

#include <ranges>
#include <vector>
auto main() -> int { std::vector v = {1,2,3,4,5,6}; int s = 0; for (auto x : v | std::views::stride(2)) s += x; return s == 9 ? 0 : 1; }
