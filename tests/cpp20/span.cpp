// feature: span
// macro: __cpp_lib_span
// standard: cpp20
// category: library
// description: std::span

#include <span>

auto sum(std::span<const int> values) -> int {
    int total = 0;
    for (auto v : values) total += v;
    return total;
}

auto main() -> int {
    int arr[] = {1, 2, 3};
    return sum(arr) - 6;
}
