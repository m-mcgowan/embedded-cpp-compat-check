// feature: structured_bindings
// macro: __cpp_structured_bindings
// standard: cpp17
// category: language
// description: Structured bindings declaration

auto main() -> int {
    int arr[2] = {1, 2};
    auto [a, b] = arr;
    return a + b - 3;
}
