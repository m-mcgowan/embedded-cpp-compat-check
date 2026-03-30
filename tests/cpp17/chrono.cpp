// feature: chrono
// macro: __cpp_lib_chrono
// standard: cpp17
// category: library
// description: Rounding functions for chrono duration and time_point

#include <chrono>
auto main() -> int { auto d = std::chrono::milliseconds(1500); auto s = std::chrono::floor<std::chrono::seconds>(d); return s.count() == 1 ? 0 : 1; }
