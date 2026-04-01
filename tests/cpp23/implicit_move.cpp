// feature: implicit_move
// macro: __cpp_implicit_move
// standard: cpp23
// category: language
// description: Simpler implicit move from local variables

struct S { S() = default; S(S&&) = default; S(const S&) = delete; };
S make() { S s; return s; }
auto main() -> int { S s = make(); (void)s; return 0; }
