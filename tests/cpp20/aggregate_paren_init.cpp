// feature: aggregate_paren_init
// macro: __cpp_aggregate_paren_init
// standard: cpp20
// category: language
// description: Aggregate initialization using parentheses

struct S { int x; int y; };
auto main() -> int { S s(1, 2); return s.x + s.y - 3; }
