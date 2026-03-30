// feature: constexpr_string_view
// macro: __cpp_lib_constexpr_string_view
// standard: cpp20
// category: library
// description: Constexpr std::string_view

#include <string_view>
constexpr std::string_view sv = "hello";
static_assert(sv.size() == 5);
auto main() -> int { return 0; }
