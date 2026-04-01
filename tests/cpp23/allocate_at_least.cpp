// feature: allocate_at_least
// macro: __cpp_lib_allocate_at_least
// standard: cpp23
// category: library
// description: std::allocator::allocate_at_least

#include <memory>
auto main() -> int { std::allocator<int> a; auto [ptr, n] = a.allocate_at_least(4); a.deallocate(ptr, n); return n >= 4 ? 0 : 1; }
