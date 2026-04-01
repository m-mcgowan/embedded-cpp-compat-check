// feature: ranges_as_rvalue
// macro: __cpp_lib_ranges_as_rvalue
// standard: cpp23
// category: library
// description: std::views::as_rvalue (move-only view)

#include <ranges>
#include <vector>
auto main() -> int { std::vector<int> v = {1,2,3}; auto r = v | std::views::as_rvalue; int s = 0; for (auto x : r) s += x; return s - 6; }
