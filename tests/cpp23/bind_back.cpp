// feature: bind_back
// macro: __cpp_lib_bind_back
// standard: cpp23
// category: library
// description: std::bind_back

#include <functional>
int sub(int a, int b) { return a - b; }
auto main() -> int { auto sub5 = std::bind_back(sub, 5); return sub5(8) - 3; }
