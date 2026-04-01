// feature: atomic_wait
// macro: __cpp_lib_atomic_wait
// standard: cpp20
// category: library
// description: std::atomic<int>::wait()

#include <atomic>
auto main() -> int { std::atomic<int> a{42}; a.wait(0); return 0; }
