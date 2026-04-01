// feature: is_pointer_interconvertible
// macro: __cpp_lib_is_pointer_interconvertible
// standard: cpp23
// category: library
// description: std::is_pointer_interconvertible_with_class

#include <type_traits>
struct S { int x; int y; };
auto main() -> int { return std::is_pointer_interconvertible_with_class<S, int>(&S::x) ? 0 : 1; }
