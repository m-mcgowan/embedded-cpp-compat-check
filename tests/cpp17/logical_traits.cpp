// feature: logical_traits
// macro: __cpp_lib_logical_traits
// standard: cpp17
// category: library
// description: Logical operations on type traits (conjunction, disjunction, negation)

#include <type_traits>
auto main() -> int { return std::conjunction_v<std::true_type, std::true_type> ? 0 : 1; }
