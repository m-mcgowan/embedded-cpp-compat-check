// feature: format_uchar
// macro: __cpp_lib_format_uchar
// standard: cpp20
// category: library
// description: Unsigned char formatting with std::format

#include <format>
auto main() -> int { unsigned char c = 65; auto s = std::format("{}", static_cast<int>(c)); return s == "65" ? 0 : 1; }
