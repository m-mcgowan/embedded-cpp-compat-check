// feature: any
// macro: __cpp_lib_any
// standard: cpp17
// category: library
// description: std::any

#include <any>

auto main() -> int {
    std::any a = 42;
    return std::any_cast<int>(a) - 42;
}
