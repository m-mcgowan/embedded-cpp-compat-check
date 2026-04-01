// feature: static_call_operator
// macro: __cpp_static_call_operator
// standard: cpp23
// category: language
// description: static operator() in function objects

struct Adder { static int operator()(int a, int b) { return a + b; } };
auto main() -> int { return Adder{}(2, 3) - 5; }
