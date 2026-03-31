// feature: atomic_ref
// macro: __cpp_lib_atomic_ref
// standard: cpp20
// category: library
// description: std::atomic_ref — atomic operations on non-atomic objects

#include <atomic>
auto main() -> int { int x = 0; std::atomic_ref<int> r(x); r.store(42); return r.load() - 42; }
