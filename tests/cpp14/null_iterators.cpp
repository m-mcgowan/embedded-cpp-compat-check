// feature: null_iterators
// macro: __cpp_lib_null_iterators
// standard: cpp14
// category: library
// description: Compare default-constructed iterators

#include <iterator>
#include <list>
auto main() -> int { std::list<int>::iterator a, b; return a == b ? 0 : 1; }
