// feature: return_type_deduction
// macro: __cpp_return_type_deduction
// standard: cpp14
// category: language
// description: Return type deduction for normal functions

auto add(int a, int b) { return a + b; }
auto main() -> int { return add(2, 3) - 5; }
