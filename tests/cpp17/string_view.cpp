// feature: string_view
// macro: __cpp_lib_string_view
// standard: cpp17
// category: library
// description: std::string_view

#include <string_view>

auto main() -> int {
    std::string_view sv = "hello";
    return static_cast<int>(sv.size()) - 5;
}
