// feature: incomplete_container_elements
// macro: __cpp_lib_incomplete_container_elements
// standard: cpp17
// category: library
// description: std::vector<struct Incomplete*> works with forward-declared types

#include <vector>
#include <forward_list>
struct Incomplete;
auto main() -> int { std::vector<Incomplete*> v; std::forward_list<Incomplete*> fl; (void)v; (void)fl; return 0; }
