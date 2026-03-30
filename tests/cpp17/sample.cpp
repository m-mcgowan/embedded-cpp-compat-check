// feature: sample
// macro: __cpp_lib_sample
// standard: cpp17
// category: library
// description: std::sample

#include <algorithm>
#include <iterator>
#include <random>
#include <vector>
auto main() -> int { std::vector<int> v = {1,2,3,4,5}; std::vector<int> out; std::sample(v.begin(), v.end(), std::back_inserter(out), 2, std::mt19937{}); return out.size() == 2 ? 0 : 1; }
