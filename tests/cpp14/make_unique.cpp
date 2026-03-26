// feature: make_unique
// macro: __cpp_lib_make_unique
// standard: cpp14
// category: library
// description: std::make_unique

#include <memory>

auto main() -> int {
    auto p = std::make_unique<int>(42);
    return *p - 42;
}
