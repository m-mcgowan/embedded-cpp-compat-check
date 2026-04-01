// feature: generic_unordered_lookup
// macro: __cpp_lib_generic_unordered_lookup
// standard: cpp20
// category: library
// description: Heterogeneous lookup in unordered containers

#include <unordered_map>
#include <string>
struct Hash { using is_transparent = void; size_t operator()(std::string_view sv) const { return std::hash<std::string_view>{}(sv); } };
struct Eq { using is_transparent = void; bool operator()(std::string_view a, std::string_view b) const { return a == b; } };
auto main() -> int { std::unordered_map<std::string, int, Hash, Eq> m; m["key"] = 42; return m.find(std::string_view("key"))->second - 42; }
