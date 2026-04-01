// feature: char8_t_lib
// macro: __cpp_lib_char8_t
// standard: cpp20
// category: library
// description: Library support for char8_t

#include <string>
auto main() -> int { std::u8string s = u8"hello"; return s.size() == 5 ? 0 : 1; }
