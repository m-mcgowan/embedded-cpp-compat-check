// feature: ranges_as_const
// macro: __cpp_lib_ranges_as_const
// standard: cpp23
// category: library
// description: std::ranges::as_const_view

#include <ranges>
#include <vector>
auto main() -> int { std::vector<int> v = {1,2,3}; auto cv = v | std::views::as_const; return *cv.begin() == 1 ? 0 : 1; }
