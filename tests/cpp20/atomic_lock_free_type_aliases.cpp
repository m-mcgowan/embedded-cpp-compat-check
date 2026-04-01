// feature: atomic_lock_free_type_aliases
// macro: __cpp_lib_atomic_lock_free_type_aliases
// standard: cpp20
// category: library
// description: std::atomic_signed_lock_free and std::atomic_unsigned_lock_free

#include <atomic>
auto main() -> int { std::atomic_signed_lock_free a{0}; a.store(42); return a.load() - 42; }
