// feature: ranges_join_with
// macro: __cpp_lib_ranges_join_with
// standard: cpp23
// category: library
// description: std::views::join_with — join ranges with a delimiter

#include <ranges>
#include <vector>
auto main() -> int { std::vector<std::vector<int>> v = {{1,2},{3,4}}; int s = 0; for (auto x : v | std::views::join_with(0)) s += x; return s == 10 ? 0 : 1; }
