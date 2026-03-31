// feature: variadic_using
// macro: __cpp_variadic_using
// standard: cpp17
// category: language
// description: Pack expansions in using-declarations

template<typename... Bases> struct Overloaded : Bases... { using Bases::operator()...; };
struct A { int operator()(int) { return 1; } };
struct B { int operator()(double) { return 2; } };
auto main() -> int { Overloaded<A, B> o; return o(1) == 1 && o(1.0) == 2 ? 0 : 1; }
