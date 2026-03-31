// feature: aligned_new
// macro: __cpp_aligned_new
// standard: cpp17
// category: language
// description: Dynamic memory allocation with over-aligned types

#include <new>
struct alignas(64) Aligned { int x; };
auto main() -> int { auto* p = new Aligned; p->x = 42; int v = p->x; delete p; return v - 42; }
