// feature: format
// macro: __cpp_lib_format
// standard: cpp20
// category: library
// description: std::format

#include <format>
#include <string>

auto main() -> int {
    auto s = std::format("{} + {} = {}", 1, 2, 3);
    return static_cast<int>(s.size()) > 0 ? 0 : 1;
}
