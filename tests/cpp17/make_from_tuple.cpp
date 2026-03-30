// feature: make_from_tuple
// macro: __cpp_lib_make_from_tuple
// standard: cpp17
// category: library
// description: std::make_from_tuple

#include <tuple>
struct S { int x; int y; S(int a, int b) : x(a), y(b) {} };
auto main() -> int { auto s = std::make_from_tuple<S>(std::make_tuple(1, 2)); return s.x + s.y - 3; }
