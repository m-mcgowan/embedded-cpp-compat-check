// feature: ranges_chunk
// macro: __cpp_lib_ranges_chunk
// standard: cpp23
// category: library
// description: std::views::chunk — partition range into fixed-size chunks

#include <ranges>
#include <vector>
auto main() -> int { std::vector v = {1,2,3,4}; int n = 0; for (auto c : v | std::views::chunk(2)) n++; return n == 2 ? 0 : 1; }
