// feature: common_reference
// macro: __cpp_lib_common_reference
// standard: cpp20
// category: library
// description: std::common_reference_t

#include <type_traits>
auto main() -> int { using T = std::common_reference_t<int&, const int&>; return std::is_same_v<T, const int&> ? 0 : 1; }
