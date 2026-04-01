// feature: atomic_value_initialization
// macro: __cpp_lib_atomic_value_initialization
// standard: cpp20
// category: library
// description: Value-initialized std::atomic<T> (zero-initialized by default)

#include <atomic>
auto main() -> int { std::atomic<int> a{}; return a.load(); }
