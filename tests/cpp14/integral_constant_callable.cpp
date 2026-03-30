// feature: integral_constant_callable
// macro: __cpp_lib_integral_constant_callable
// standard: cpp14
// category: library
// description: std::integral_constant::operator()

#include <type_traits>
auto main() -> int { std::true_type t; return t() ? 0 : 1; }
