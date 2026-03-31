// feature: atomic_is_always_lock_free
// macro: __cpp_lib_atomic_is_always_lock_free
// standard: cpp17
// category: library
// description: std::atomic<T>::is_always_lock_free

#include <atomic>
auto main() -> int { (void)std::atomic<int>::is_always_lock_free; return 0; }
