// feature: constexpr_complex
// macro: __cpp_lib_constexpr_complex
// standard: cpp20
// category: library
// description: constexpr std::complex operations

#include <complex>
constexpr std::complex<double> c{1.0, 2.0};
static_assert(c.real() == 1.0);
auto main() -> int { return 0; }
