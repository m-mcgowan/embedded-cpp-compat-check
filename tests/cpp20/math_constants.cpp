// feature: math_constants
// macro: __cpp_lib_math_constants
// standard: cpp20
// category: library
// description: Mathematical constants
#include <numbers>
auto main() -> int {
    double pi = std::numbers::pi;
    return (pi > 3.14 && pi < 3.15) ? 0 : 1;
}
