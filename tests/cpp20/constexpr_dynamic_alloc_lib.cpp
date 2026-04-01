// feature: constexpr_dynamic_alloc_lib
// macro: __cpp_lib_constexpr_dynamic_alloc
// standard: cpp20
// category: library
// description: constexpr std::allocator

#include <memory>
constexpr int f() { std::allocator<int> a; int* p = a.allocate(1); *p = 42; int v = *p; a.deallocate(p, 1); return v; }
static_assert(f() == 42);
auto main() -> int { return 0; }
