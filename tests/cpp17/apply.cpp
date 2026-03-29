// feature: apply
// macro: __cpp_lib_apply
// standard: cpp17
// category: library
// description: std::apply

#include <tuple>

int add(int a, int b) { return a + b; }

auto main() -> int {
    auto args = std::make_tuple(2, 3);
    return std::apply(add, args) - 5;
}
