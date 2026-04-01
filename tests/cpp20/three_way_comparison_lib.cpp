// feature: three_way_comparison_lib
// macro: __cpp_lib_three_way_comparison
// standard: cpp20
// category: library
// description: Three-way comparison library support (<compare>)

#include <compare>
auto main() -> int { auto r = (1 <=> 2); return (r < 0) ? 0 : 1; }
