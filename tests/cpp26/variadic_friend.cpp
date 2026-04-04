// feature: variadic_friend
// macro: __cpp_variadic_friend
// standard: cpp26
// category: language
// description: Variadic friend declarations

struct A {}; struct B {};
template<typename... Ts> struct S { friend Ts...; int x = 42; };
auto main() -> int { return 0; }
