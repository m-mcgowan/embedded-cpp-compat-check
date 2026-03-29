// feature: lambdas
// macro: __cpp_lambdas
// standard: cpp11
// category: language
// description: Lambda expressions

auto main() -> int {
    auto add = [](int a, int b) { return a + b; };
    return add(2, 3) - 5;
}
