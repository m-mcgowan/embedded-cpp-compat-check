// feature: inplace_vector
// macro: __cpp_lib_inplace_vector
// standard: cpp26
// category: library
// description: std::inplace_vector

#include <inplace_vector>
auto main() -> int { std::inplace_vector<int, 8> v; v.push_back(42); return v[0] - 42; }
