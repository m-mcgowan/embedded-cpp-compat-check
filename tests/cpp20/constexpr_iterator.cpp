// feature: constexpr_iterator
// macro: __cpp_lib_constexpr_iterator
// standard: cpp20
// category: library
// description: constexpr iterator operations

#include <iterator>
#include <array>
constexpr int f() { std::array<int, 3> a = {1, 2, 3}; return *std::begin(a); }
static_assert(f() == 1);
auto main() -> int { return 0; }
