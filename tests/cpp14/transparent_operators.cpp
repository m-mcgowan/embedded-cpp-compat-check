// feature: transparent_operators
// macro: __cpp_lib_transparent_operators
// standard: cpp14
// category: library
// description: Transparent function objects (std::less<> etc)

#include <functional>
auto main() -> int { std::less<> cmp; return cmp(1, 2) ? 0 : 1; }
