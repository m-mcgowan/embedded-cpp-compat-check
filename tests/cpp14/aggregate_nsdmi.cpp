// feature: aggregate_nsdmi
// macro: __cpp_aggregate_nsdmi
// standard: cpp14
// category: language
// description: Aggregate classes with default member initializers

struct S { int x = 1; int y = 2; };
auto main() -> int { S s{10}; return s.x + s.y - 12; }
