// feature: variant
// macro: __cpp_lib_variant
// standard: cpp17
// category: library
// description: std::variant

#include <variant>

auto main() -> int {
    std::variant<int, float> v = 42;
    return std::get<int>(v) - 42;
}
