// feature: remove_cvref
// macro: __cpp_lib_remove_cvref
// standard: cpp20
// category: library
// description: std::remove_cvref

#include <type_traits>
auto main() -> int { return std::is_same_v<std::remove_cvref_t<const int&>, int> ? 0 : 1; }
