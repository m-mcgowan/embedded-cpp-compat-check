// feature: generic_associative_lookup
// macro: __cpp_lib_generic_associative_lookup
// standard: cpp14
// category: library
// description: Heterogeneous comparison lookup in associative containers

#include <map>
#include <string>
#include <string_view>
auto main() -> int { std::map<std::string, int, std::less<>> m; m["key"] = 42; return m.count(std::string_view("key")) == 1 ? 0 : 1; }
