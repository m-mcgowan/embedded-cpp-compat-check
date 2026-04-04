// feature: exchange_function
// macro: __cpp_lib_exchange_function
// standard: cpp14
// category: library
// description: std::exchange

#include <utility>
auto main() -> int { int x = 42; int old = std::exchange(x, 0); return old - 42; }
