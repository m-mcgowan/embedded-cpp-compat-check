// feature: invoke
// macro: __cpp_lib_invoke
// standard: cpp17
// category: library
// description: std::invoke

#include <functional>

int add(int a, int b) { return a + b; }

auto main() -> int {
    return std::invoke(add, 2, 3) - 5;
}
