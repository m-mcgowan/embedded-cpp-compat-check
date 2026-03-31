// feature: ranges_zip
// macro: __cpp_lib_ranges_zip
// standard: cpp23
// category: library
// description: std::views::zip

#include <ranges>
#include <vector>
auto main() -> int { std::vector a = {1,2,3}; std::vector b = {4,5,6}; int s = 0; for (auto [x,y] : std::views::zip(a, b)) s += x + y; return s - 21; }
