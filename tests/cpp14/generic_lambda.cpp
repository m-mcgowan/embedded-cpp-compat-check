// feature: generic_lambda
// macro: __cpp_generic_lambdas
// standard: cpp14
// category: language
// description: Generic (polymorphic) lambdas

auto main() -> int {
    auto add = [](auto a, auto b) { return a + b; };
    return add(1, 2) - 3;
}
