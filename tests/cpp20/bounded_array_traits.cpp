// feature: bounded_array_traits
// macro: __cpp_lib_bounded_array_traits
// standard: cpp20
// category: library
// description: std::is_bounded_array and std::is_unbounded_array

#include <type_traits>
auto main() -> int { return std::is_bounded_array_v<int[3]> && !std::is_bounded_array_v<int[]> ? 0 : 1; }
