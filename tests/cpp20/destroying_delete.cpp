// feature: destroying_delete
// macro: __cpp_lib_destroying_delete
// standard: cpp20
// category: library
// description: Destroying operator delete (library support: std::destroying_delete_t)

#include <new>
struct Node { int v; static void operator delete(Node* p, std::destroying_delete_t) { p->~Node(); ::operator delete(p); } };
auto main() -> int { auto* n = new Node{42}; delete n; return 0; }
