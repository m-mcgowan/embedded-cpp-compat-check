// feature: unreachable
// macro: __cpp_lib_unreachable
// standard: cpp23
// category: library
// description: std::unreachable

#include <utility>
auto main() -> int { int x = 1; if (x == 1) return 0; std::unreachable(); }
