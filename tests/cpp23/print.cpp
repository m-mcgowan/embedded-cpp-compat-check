// feature: print
// macro: __cpp_lib_print
// standard: cpp23
// category: library
// description: std::print

#include <print>
#include <string>

auto main() -> int {
    auto s = std::format("{}", 42);
    return static_cast<int>(s.size()) > 0 ? 0 : 1;
}
