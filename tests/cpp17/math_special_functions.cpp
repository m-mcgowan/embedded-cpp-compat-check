// feature: math_special_functions
// macro: __cpp_lib_math_special_functions
// standard: cpp17
// category: library
// description: Mathematical special functions (std::cyl_bessel_j etc)

#include <cmath>
auto main() -> int { double v = std::riemann_zeta(2.0); return v > 1.6 && v < 1.7 ? 0 : 1; }
