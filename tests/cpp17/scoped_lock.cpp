// feature: scoped_lock
// macro: __cpp_lib_scoped_lock
// standard: cpp17
// category: library
// description: std::scoped_lock
#include <mutex>
auto main() -> int {
    std::mutex m;
    std::scoped_lock lock(m);
    return 0;
}
