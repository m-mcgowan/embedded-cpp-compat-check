// feature: ranges_find_last
// macro: __cpp_lib_ranges_find_last
// standard: cpp23
// category: library
// description: std::ranges::find_last

#include <algorithm>
#include <vector>
auto main() -> int { std::vector v = {1,2,3,2,1}; auto r = std::ranges::find_last(v, 2); return *r.begin() == 2 && r.begin() == v.begin()+3 ? 0 : 1; }
