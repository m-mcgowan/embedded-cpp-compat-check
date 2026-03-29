// feature: bind_front
// macro: __cpp_lib_bind_front
// standard: cpp20
// category: library
// description: std::bind_front

#include <functional>

int add(int a, int b) { return a + b; }

auto main() -> int {
    auto add5 = std::bind_front(add, 5);
    return add5(3) - 8;
}
