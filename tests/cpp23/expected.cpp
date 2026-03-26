// feature: expected
// macro: __cpp_lib_expected
// standard: cpp23
// category: library
// description: std::expected

#include <expected>

auto divide(int a, int b) -> std::expected<int, const char*> {
    if (b == 0) return std::unexpected("division by zero");
    return a / b;
}

auto main() -> int {
    auto r = divide(6, 3);
    return r.value() - 2;
}
