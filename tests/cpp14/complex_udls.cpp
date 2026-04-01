// feature: complex_udls
// macro: __cpp_lib_complex_udls
// standard: cpp14
// category: library
// description: User-defined literals for std::complex (1i, 1if, etc)

#include <complex>
using namespace std::complex_literals;
auto main() -> int { auto c = 1.0i; return c.imag() == 1.0 ? 0 : 1; }
