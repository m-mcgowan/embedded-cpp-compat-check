// feature: sized_deallocation
// macro: __cpp_sized_deallocation
// standard: cpp14
// category: language
// description: Sized deallocation operator delete(void*, size_t)

#include <cstddef>
struct S { int v; static void operator delete(void* p, std::size_t) noexcept { ::operator delete(p); } };
auto main() -> int { S* p = new S{42}; delete p; return 0; }
