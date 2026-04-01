// feature: is_implicit_lifetime
// macro: __cpp_lib_is_implicit_lifetime
// standard: cpp23
// category: library
// description: std::is_implicit_lifetime type trait

#include <type_traits>
struct S { int x; };
auto main() -> int { return std::is_implicit_lifetime_v<S> ? 0 : 1; }
