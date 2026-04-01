// feature: ranges_cartesian_product
// macro: __cpp_lib_ranges_cartesian_product
// standard: cpp23
// category: library
// description: std::ranges::cartesian_product_view

#include <ranges>
#include <vector>
auto main() -> int { std::vector a = {1,2}; std::vector b = {3,4}; int n = 0; for (auto [x,y] : std::views::cartesian_product(a, b)) n++; return n == 4 ? 0 : 1; }
