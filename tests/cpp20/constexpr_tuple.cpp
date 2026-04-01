// feature: constexpr_tuple
// macro: __cpp_lib_constexpr_tuple
// standard: cpp20
// category: library
// description: constexpr std::tuple

#include <tuple>
constexpr auto t = std::make_tuple(1, 2, 3);
static_assert(std::get<0>(t) == 1);
auto main() -> int { return 0; }
