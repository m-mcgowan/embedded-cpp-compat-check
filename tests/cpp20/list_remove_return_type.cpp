// feature: list_remove_return_type
// macro: __cpp_lib_list_remove_return_type
// standard: cpp20
// category: library
// description: std::list::remove returns removed count

#include <list>
auto main() -> int { std::list<int> l = {1, 2, 2, 3}; auto n = l.remove(2); return n == 2 ? 0 : 1; }
