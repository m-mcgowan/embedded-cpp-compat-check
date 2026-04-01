// feature: constexpr_utility
// macro: __cpp_lib_constexpr_utility
// standard: cpp20
// category: library
// description: constexpr std::pair, std::exchange

#include <utility>
constexpr int f() { int x = 1; int old = std::exchange(x, 42); return x + old; }
static_assert(f() == 43);
auto main() -> int { return 0; }
