// feature: to_address
// macro: __cpp_lib_to_address
// standard: cpp20
// category: library
// description: std::to_address

#include <memory>
auto main() -> int { int x = 42; int* p = &x; return *std::to_address(p) - 42; }
