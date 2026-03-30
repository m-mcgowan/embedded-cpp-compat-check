// feature: is_final
// macro: __cpp_lib_is_final
// standard: cpp14
// category: library
// description: std::is_final

#include <type_traits>
struct A {}; struct B final {};
auto main() -> int { return std::is_final<B>::value && !std::is_final<A>::value ? 0 : 1; }
