// feature: hypot
// macro: __cpp_lib_hypot
// standard: cpp17
// category: library
// description: 3-argument overload of std::hypot

#include <cmath>
auto main() -> int { double h = std::hypot(1.0, 2.0, 2.0); return h > 2.9 && h < 3.1 ? 0 : 1; }
