// feature: tuple_like
// macro: __cpp_lib_tuple_like
// standard: cpp23
// category: library
// description: Tuple protocol for std::pair, std::array, std::subrange

#include <tuple>
#include <utility>
auto main() -> int { auto p = std::pair(1, 2); auto [a, b] = p; return a + b - 3; }
