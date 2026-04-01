// feature: constexpr_dynamic_alloc
// macro: __cpp_constexpr_dynamic_alloc
// standard: cpp20
// category: language
// description: constexpr new/delete in constant expressions

constexpr int f() { int* p = new int(42); int v = *p; delete p; return v; }
static_assert(f() == 42);
auto main() -> int { return 0; }
