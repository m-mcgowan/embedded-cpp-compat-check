// feature: constexpr_string
// macro: __cpp_lib_constexpr_string
// standard: cpp20
// category: library
// description: Constexpr std::string

#include <string>
constexpr int f() { std::string s = "hi"; return s.size(); }
static_assert(f() == 2);
auto main() -> int { return 0; }
