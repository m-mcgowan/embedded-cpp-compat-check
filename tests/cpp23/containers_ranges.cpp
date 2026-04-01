// feature: containers_ranges
// macro: __cpp_lib_containers_ranges
// standard: cpp23
// category: library
// description: Construct containers from ranges

#include <vector>
#include <ranges>
auto main() -> int { auto r = std::views::iota(1, 4); std::vector<int> v(r.begin(), r.end()); return v.size() == 3 && v[0] == 1 ? 0 : 1; }
