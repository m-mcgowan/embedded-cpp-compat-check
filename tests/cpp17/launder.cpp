// feature: launder
// macro: __cpp_lib_launder
// standard: cpp17
// category: library
// description: std::launder

#include <new>
auto main() -> int { int x = 42; auto* p = std::launder(&x); return *p - 42; }
