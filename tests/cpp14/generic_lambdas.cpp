// feature: generic_lambdas
// macro: __cpp_generic_lambdas
// standard: cpp14
// category: language
// description: Generic lambda expressions

auto main() -> int { auto add = [](auto a, auto b) { return a + b; }; return add(2, 3) - 5; }
