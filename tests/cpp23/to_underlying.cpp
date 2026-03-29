// feature: to_underlying
// macro: __cpp_lib_to_underlying
// standard: cpp23
// category: library
// description: std::to_underlying

#include <utility>

enum class Color : int { Red = 1, Green = 2, Blue = 3 };

auto main() -> int {
    return std::to_underlying(Color::Green) - 2;
}
