// feature: robust_nonmodifying_seq_ops
// macro: __cpp_lib_robust_nonmodifying_seq_ops
// standard: cpp14
// category: library
// description: Two-range overloads of std::equal and std::is_permutation

#include <algorithm>
#include <vector>
auto main() -> int { std::vector<int> a = {1,2,3}, b = {1,2,3}; return std::equal(a.begin(), a.end(), b.begin(), b.end()) ? 0 : 1; }
