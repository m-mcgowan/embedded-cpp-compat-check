// feature: ranges_chunk_by
// macro: __cpp_lib_ranges_chunk_by
// standard: cpp23
// category: library
// description: std::views::chunk_by — partition range by adjacent predicate

#include <ranges>
#include <vector>
auto main() -> int { std::vector v = {1,1,2,2,3}; int n = 0; for (auto c : v | std::views::chunk_by(std::equal_to<>{})) n++; return n == 3 ? 0 : 1; }
