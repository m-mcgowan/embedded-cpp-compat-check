// feature: ranges_repeat
// macro: __cpp_lib_ranges_repeat
// standard: cpp23
// category: library
// description: std::views::repeat

#include <ranges>
auto main() -> int { int n = 0; for (auto x : std::views::repeat(42) | std::views::take(3)) n += x; return n == 126 ? 0 : 1; }
