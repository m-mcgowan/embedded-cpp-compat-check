// feature: nonmember_container_access
// macro: __cpp_lib_nonmember_container_access
// standard: cpp17
// category: library
// description: std::size(), std::data(), std::empty()

#include <iterator>
auto main() -> int { int a[] = {1,2,3}; return std::size(a) == 3 ? 0 : 1; }
