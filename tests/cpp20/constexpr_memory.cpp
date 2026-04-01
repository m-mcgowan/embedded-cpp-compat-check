// feature: constexpr_memory
// macro: __cpp_lib_constexpr_memory
// standard: cpp20
// category: library
// description: constexpr std::construct_at

#include <memory>
constexpr int f() { int x = 0; std::construct_at(&x, 42); return x; }
static_assert(f() == 42);
auto main() -> int { return 0; }
