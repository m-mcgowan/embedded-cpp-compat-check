// feature: move_iterator_concept
// macro: __cpp_lib_move_iterator_concept
// standard: cpp20
// category: library
// description: std::move_iterator satisfies iterator concepts

#include <iterator>
#include <vector>
auto main() -> int { std::vector<int> v = {1,2,3}; auto it = std::make_move_iterator(v.begin()); (void)it; return 0; }
