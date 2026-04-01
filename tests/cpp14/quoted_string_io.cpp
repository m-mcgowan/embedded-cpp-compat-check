// feature: quoted_string_io
// macro: __cpp_lib_quoted_string_io
// standard: cpp14
// category: library
// description: std::quoted for I/O of quoted strings

#include <iomanip>
#include <sstream>
auto main() -> int { std::ostringstream oss; oss << std::quoted("hello"); return oss.str() == "\"hello\"" ? 0 : 1; }
