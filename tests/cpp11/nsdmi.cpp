// feature: nsdmi
// macro: __cpp_nsdmi
// standard: cpp11
// category: language
// description: Non-static data member initializers

struct S { int x = 42; };
auto main() -> int { S s; return s.x - 42; }
