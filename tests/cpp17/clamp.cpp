// feature: clamp
// macro: __cpp_lib_clamp
// standard: cpp17
// category: library
// description: std::clamp

#include <algorithm>

auto main() -> int {
    int val = std::clamp(150, 0, 100);
    return val - 100;
}
