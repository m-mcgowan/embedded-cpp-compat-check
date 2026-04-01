// feature: constexpr_functional
// macro: __cpp_lib_constexpr_functional
// standard: cpp20
// category: library
// description: constexpr std::invoke

#include <functional>
constexpr int add(int a, int b) { return a + b; }
static_assert(std::invoke(add, 2, 3) == 5);
auto main() -> int { return 0; }
