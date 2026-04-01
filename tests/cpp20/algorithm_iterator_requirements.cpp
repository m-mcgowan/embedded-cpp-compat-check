// feature: algorithm_iterator_requirements
// macro: __cpp_lib_algorithm_iterator_requirements
// standard: cpp20
// category: library
// description: Relaxed iterator requirements for algorithms

#include <algorithm>
#include <vector>
auto main() -> int { std::vector<int> v = {3,1,2}; std::sort(v.begin(), v.end()); return v[0] == 1 ? 0 : 1; }
