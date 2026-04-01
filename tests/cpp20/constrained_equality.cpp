// feature: constrained_equality
// macro: __cpp_lib_constrained_equality
// standard: cpp20
// category: library
// description: Constrained equality for utility types

#include <utility>
#include <optional>
auto main() -> int { std::optional<int> a{42}, b{42}; return a == b ? 0 : 1; }
