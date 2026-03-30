// feature: invoke_r
// macro: __cpp_lib_invoke_r
// standard: cpp23
// category: library
// description: std::invoke_r

#include <functional>
int add(int a, int b) { return a+b; }
auto main() -> int { return std::invoke_r<long>(add, 2, 3) - 5; }
