// feature: string_udls
// macro: __cpp_lib_string_udls
// standard: cpp14
// category: library
// description: User-defined literals for std::string ("hello"s)

#include <string>
using namespace std::string_literals;
auto main() -> int { auto s = "hello"s; return s.size() == 5 ? 0 : 1; }
