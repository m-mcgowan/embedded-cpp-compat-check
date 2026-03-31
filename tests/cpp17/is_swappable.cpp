// feature: is_swappable
// macro: __cpp_lib_is_swappable
// standard: cpp17
// category: library
// description: std::is_swappable and std::is_nothrow_swappable

#include <type_traits>
auto main() -> int { return std::is_swappable_v<int> ? 0 : 1; }
