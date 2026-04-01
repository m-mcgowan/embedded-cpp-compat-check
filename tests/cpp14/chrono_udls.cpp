// feature: chrono_udls
// macro: __cpp_lib_chrono_udls
// standard: cpp14
// category: library
// description: User-defined literals for chrono duration types (1s, 1ms, etc)

#include <chrono>
using namespace std::chrono_literals;
auto main() -> int { auto d = 1s; return d.count() == 1 ? 0 : 1; }
