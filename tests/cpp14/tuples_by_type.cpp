// feature: tuples_by_type
// macro: __cpp_lib_tuples_by_type
// standard: cpp14
// category: library
// description: Addressing tuple elements by type

#include <tuple>
auto main() -> int { auto t = std::make_tuple(42, 3.14); return std::get<int>(t) - 42; }
