// feature: polymorphic_allocator
// macro: __cpp_lib_polymorphic_allocator
// standard: cpp20
// category: library
// description: std::pmr::polymorphic_allocator

#include <memory_resource>
auto main() -> int { std::pmr::polymorphic_allocator<int> alloc; return 0; }
