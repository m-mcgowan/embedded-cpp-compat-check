// feature: is_constant_evaluated
// macro: __cpp_lib_is_constant_evaluated
// standard: cpp20
// category: library
// description: std::is_constant_evaluated

#include <type_traits>
constexpr int f() { if (std::is_constant_evaluated()) return 1; return 0; }
auto main() -> int { constexpr int v = f(); return v == 1 ? 0 : 1; }
