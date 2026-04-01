// feature: atomic_flag_test
// macro: __cpp_lib_atomic_flag_test
// standard: cpp20
// category: library
// description: std::atomic_flag::test()

#include <atomic>
auto main() -> int { std::atomic_flag f = ATOMIC_FLAG_INIT; return f.test() ? 1 : 0; }
