// feature: shared_ptr_arrays
// macro: __cpp_lib_shared_ptr_arrays
// standard: cpp17
// category: library
// description: std::shared_ptr<T[]>
#include <memory>
auto main() -> int {
    auto p = std::make_shared<int[]>(3);
    p[0] = 42;
    return p[0] - 42;
}
