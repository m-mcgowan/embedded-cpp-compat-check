// feature: flat_map
// macro: __cpp_lib_flat_map
// standard: cpp23
// category: library
// description: std::flat_map

#include <flat_map>
auto main() -> int { std::flat_map<int,int> m; m[1] = 42; return m[1] - 42; }
