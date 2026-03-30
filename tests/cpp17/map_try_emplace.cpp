// feature: map_try_emplace
// macro: __cpp_lib_map_try_emplace
// standard: cpp17
// category: library
// description: std::map::try_emplace
#include <map>
#include <string>
auto main() -> int {
    std::map<int, int> m;
    m.try_emplace(1, 42);
    return m[1] - 42;
}
