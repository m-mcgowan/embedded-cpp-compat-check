// feature: constexpr_bitset
// macro: __cpp_lib_constexpr_bitset
// standard: cpp23
// category: library
// description: Constexpr std::bitset

#include <bitset>
constexpr std::bitset<8> b(0b10101010);
static_assert(b.count() == 4);
auto main() -> int { return 0; }
