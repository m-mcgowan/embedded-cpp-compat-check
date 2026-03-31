// feature: hardware_interference_size
// macro: __cpp_lib_hardware_interference_size
// standard: cpp17
// category: library
// description: std::hardware_destructive_interference_size

#include <new>
auto main() -> int { return std::hardware_destructive_interference_size > 0 ? 0 : 1; }
