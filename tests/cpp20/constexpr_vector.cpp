// feature: constexpr_vector
// macro: __cpp_lib_constexpr_vector
// standard: cpp20
// category: library
// description: Constexpr std::vector

#include <vector>
constexpr int f() { std::vector<int> v = {1,2,3}; return v.size(); }
static_assert(f() == 3);
auto main() -> int { return 0; }
