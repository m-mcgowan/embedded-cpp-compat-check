// feature: is_layout_compatible
// macro: __cpp_lib_is_layout_compatible
// standard: cpp23
// category: library
// description: std::is_layout_compatible type trait

#include <type_traits>
struct A { int x; }; struct B { int y; };
auto main() -> int { return std::is_layout_compatible_v<A, B> ? 0 : 1; }
