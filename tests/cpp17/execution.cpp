// feature: execution
// macro: __cpp_lib_execution
// standard: cpp17
// category: library
// description: Execution policies for parallel algorithms

#include <execution>
#include <algorithm>
#include <vector>
auto main() -> int { std::vector<int> v = {3,1,2}; std::sort(std::execution::seq, v.begin(), v.end()); return v[0] == 1 ? 0 : 1; }
