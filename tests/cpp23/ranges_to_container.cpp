// feature: ranges_to_container
// macro: __cpp_lib_ranges_to_container
// standard: cpp23
// category: library
// description: std::ranges::to — convert range to container

#include <ranges>
#include <vector>
auto main() -> int { auto v = std::views::iota(1, 4) | std::ranges::to<std::vector>(); return v.size() == 3 && v[0] == 1 ? 0 : 1; }
