// feature: to_array
// macro: __cpp_lib_to_array
// standard: cpp20
// category: library
// description: std::to_array

#include <array>

auto main() -> int {
    auto arr = std::to_array({1, 2, 3, 4, 5});
    return arr[2] - 3;
}
