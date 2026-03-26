// feature: ranges
// macro: __cpp_lib_ranges
// standard: cpp20
// category: library
// description: Ranges library

#include <ranges>
#include <array>

auto main() -> int {
    std::array arr = {1, 2, 3, 4, 5};
    int total = 0;
    for (auto x : arr | std::views::take(3)) total += x;
    return total - 6;
}
