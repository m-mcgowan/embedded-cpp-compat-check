// feature: string_contains
// macro: __cpp_lib_string_contains
// standard: cpp23
// category: library
// description: string::contains

#include <string>
auto main() -> int { std::string s = "hello world"; return s.contains("world") ? 0 : 1; }
