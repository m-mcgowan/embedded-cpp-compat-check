// feature: impl_destroying_delete
// macro: __cpp_impl_destroying_delete
// standard: cpp20
// category: language
// description: Destroying operator delete (compiler support)

#include <new>
struct S { int v; static void operator delete(S* p, std::destroying_delete_t) { p->~S(); ::operator delete(p); } };
auto main() -> int { auto* p = new S{42}; delete p; return 0; }
