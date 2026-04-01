// feature: ranges_enumerate
// macro: __cpp_lib_ranges_enumerate
// standard: cpp23
// category: library
// description: std::ranges::enumerate_view

#include <ranges>
#include <vector>
auto main() -> int { std::vector v = {10,20,30}; int s = 0; for (auto [i, x] : std::views::enumerate(v)) s += i; return s == 3 ? 0 : 1; }
