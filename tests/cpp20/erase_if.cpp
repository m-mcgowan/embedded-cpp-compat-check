// feature: erase_if
// macro: __cpp_lib_erase_if
// standard: cpp20
// category: library
// description: std::erase/std::erase_if
#include <vector>
auto main() -> int {
    std::vector<int> v = {1, 2, 3, 4, 5};
    std::erase_if(v, [](int x) { return x % 2 == 0; });
    return static_cast<int>(v.size()) - 3;
}
