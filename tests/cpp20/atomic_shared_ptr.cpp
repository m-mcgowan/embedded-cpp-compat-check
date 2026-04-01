// feature: atomic_shared_ptr
// macro: __cpp_lib_atomic_shared_ptr
// standard: cpp20
// category: library
// description: std::atomic<std::shared_ptr<int>>

#include <atomic>
#include <memory>
auto main() -> int { std::atomic<std::shared_ptr<int>> a; a.store(std::make_shared<int>(42)); return *a.load() - 42; }
