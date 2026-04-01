// feature: atomic_float
// macro: __cpp_lib_atomic_float
// standard: cpp20
// category: library
// description: std::atomic<float>

#include <atomic>
auto main() -> int { std::atomic<float> a{1.0f}; a.store(42.0f); return static_cast<int>(a.load()) - 42; }
