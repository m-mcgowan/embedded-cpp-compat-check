// feature: integer_comparison_functions
// macro: __cpp_lib_integer_comparison_functions
// standard: cpp20
// category: library
// description: Safe integer comparison (cmp_less etc)

#include <utility>
auto main() -> int { return std::cmp_less(-1, 1u) ? 0 : 1; }
