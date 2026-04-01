// feature: ranges_slide
// macro: __cpp_lib_ranges_slide
// standard: cpp23
// category: library
// description: std::ranges::slide_view

#include <ranges>
#include <vector>
auto main() -> int { std::vector v = {1,2,3,4}; int n = 0; for (auto w : v | std::views::slide(2)) n++; return n == 3 ? 0 : 1; }
