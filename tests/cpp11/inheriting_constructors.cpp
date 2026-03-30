// feature: inheriting_constructors
// macro: __cpp_inheriting_constructors
// standard: cpp11
// category: language
// description: Inheriting constructors

struct Base { int v; Base(int x) : v(x) {} };
struct Derived : Base { using Base::Base; };
auto main() -> int { Derived d(42); return d.v - 42; }
