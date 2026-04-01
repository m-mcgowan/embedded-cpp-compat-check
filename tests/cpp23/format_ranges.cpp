// feature: format_ranges
// macro: __cpp_lib_format_ranges
// standard: cpp23
// category: library
// description: Format ranges with std::format

#include <format>
#include <vector>
auto main() -> int { std::vector<int> v = {1, 2, 3}; auto s = std::format("{}", v); return s.empty() ? 1 : 0; }
