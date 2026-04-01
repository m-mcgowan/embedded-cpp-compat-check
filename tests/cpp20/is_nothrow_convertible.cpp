// feature: is_nothrow_convertible
// macro: __cpp_lib_is_nothrow_convertible
// standard: cpp20
// category: library
// description: std::is_nothrow_convertible

#include <type_traits>
auto main() -> int { return std::is_nothrow_convertible_v<int, double> ? 0 : 1; }
