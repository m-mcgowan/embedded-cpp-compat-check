// feature: flat_set
// macro: __cpp_lib_flat_set
// standard: cpp23
// category: library
// description: std::flat_set

#include <flat_set>
auto main() -> int { std::flat_set<int> s = {3, 1, 2}; return *s.begin() == 1 ? 0 : 1; }
