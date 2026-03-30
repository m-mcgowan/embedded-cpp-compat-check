// feature: int_pow2
// macro: __cpp_lib_int_pow2
// standard: cpp20
// category: library
// description: Integral power-of-2 operations (bit_ceil, has_single_bit, etc)

#include <bit>
auto main() -> int { return std::has_single_bit(8u) && std::bit_ceil(5u) == 8 ? 0 : 1; }
