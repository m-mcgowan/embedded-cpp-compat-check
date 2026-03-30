// feature: tuple_element_t
// macro: __cpp_lib_tuple_element_t
// standard: cpp14
// category: library
// description: std::tuple_element_t

#include <tuple>
auto main() -> int { using T = std::tuple<int, double>; std::tuple_element_t<0, T> x = 42; return x - 42; }
