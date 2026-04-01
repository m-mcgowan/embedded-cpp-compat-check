// feature: aggregate_bases
// macro: __cpp_aggregate_bases
// standard: cpp17
// category: language
// description: Aggregate classes with public base classes

struct Base { int x; };
struct Derived : Base { int y; };
auto main() -> int { Derived d{{1}, 2}; return d.x + d.y - 3; }
