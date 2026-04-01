// feature: associative_heterogeneous_erasure
// macro: __cpp_lib_associative_heterogeneous_erasure
// standard: cpp23
// category: library
// description: std::map::erase with transparent comparator

#include <map>
#include <string>
#include <string_view>
auto main() -> int { std::map<std::string, int, std::less<>> m; m["key"] = 42; m.erase(std::string_view("key")); return m.empty() ? 0 : 1; }
