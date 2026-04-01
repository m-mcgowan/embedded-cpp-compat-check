// feature: allocator_traits_is_always_equal
// macro: __cpp_lib_allocator_traits_is_always_equal
// standard: cpp11
// category: library
// description: std::allocator_traits<std::allocator<int>>::is_always_equal

#include <memory>
auto main() -> int { return std::allocator_traits<std::allocator<int>>::is_always_equal::value ? 0 : 1; }
