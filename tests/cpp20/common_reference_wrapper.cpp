// feature: common_reference_wrapper
// macro: __cpp_lib_common_reference_wrapper
// standard: cpp20
// category: library
// description: std::common_reference with reference_wrapper

#include <type_traits>
#include <functional>
auto main() -> int { using T = std::common_reference_t<int&, std::reference_wrapper<int>>; return std::is_reference_v<T> ? 0 : 1; }
