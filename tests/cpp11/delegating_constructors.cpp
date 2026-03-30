// feature: delegating_constructors
// macro: __cpp_delegating_constructors
// standard: cpp11
// category: language
// description: Delegating constructors

struct S { int v; S(int x) : v(x) {} S() : S(42) {} };
auto main() -> int { S s; return s.v - 42; }
