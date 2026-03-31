// feature: barrier
// macro: __cpp_lib_barrier
// standard: cpp20
// category: library
// description: std::barrier — reusable thread barrier

#include <barrier>
auto main() -> int { std::barrier b(1); b.arrive_and_drop(); return 0; }
