// feature: shift
// macro: __cpp_lib_shift
// standard: cpp20
// category: library
// description: std::shift_left and std::shift_right

#include <algorithm>
#include <vector>
auto main() -> int { std::vector v = {1,2,3,4,5}; std::shift_left(v.begin(), v.end(), 2); return v[0] == 3 ? 0 : 1; }
