// feature: make_reverse_iterator
// macro: __cpp_lib_make_reverse_iterator
// standard: cpp14
// category: library
// description: std::make_reverse_iterator

#include <iterator>
#include <vector>
auto main() -> int { std::vector<int> v = {1,2,3}; auto rit = std::make_reverse_iterator(v.end()); return *rit - 3; }
