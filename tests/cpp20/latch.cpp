// feature: latch
// macro: __cpp_lib_latch
// standard: cpp20
// category: library
// description: std::latch — single-use countdown synchronization

#include <latch>
auto main() -> int { std::latch l(1); l.count_down(); return l.try_wait() ? 0 : 1; }
