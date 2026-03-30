// feature: ssize
// macro: __cpp_lib_ssize
// standard: cpp20
// category: library
// description: std::ssize

#include <iterator>
auto main() -> int { int a[] = {1,2,3}; return std::ssize(a) == 3 ? 0 : 1; }
