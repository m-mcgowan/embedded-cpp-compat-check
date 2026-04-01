// feature: unordered_map_try_emplace
// macro: __cpp_lib_unordered_map_try_emplace
// standard: cpp17
// category: library
// description: std::unordered_map::try_emplace and insert_or_assign

#include <unordered_map>
#include <string>
auto main() -> int { std::unordered_map<std::string, int> m; m.try_emplace("key", 42); return m["key"] - 42; }
