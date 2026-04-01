// feature: adaptor_iterator_pair_constructor
// macro: __cpp_lib_adaptor_iterator_pair_constructor
// standard: cpp23
// category: library
// description: Iterator-pair constructors for std::stack and std::queue

#include <queue>
#include <vector>
auto main() -> int { std::vector<int> v = {1,2,3}; std::queue<int> q(v.begin(), v.end()); return q.size() == 3 ? 0 : 1; }
