// feature: impl_three_way_comparison
// macro: __cpp_impl_three_way_comparison
// standard: cpp20
// category: language
// description: Three-way comparison (spaceship operator)

#include <compare>
struct S { int v; auto operator<=>(const S&) const = default; };
auto main() -> int { S a{1}, b{2}; return (a <=> b) < 0 ? 0 : 1; }
