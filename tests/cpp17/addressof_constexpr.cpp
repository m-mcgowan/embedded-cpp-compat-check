// feature: addressof_constexpr
// macro: __cpp_lib_addressof_constexpr
// standard: cpp17
// category: library
// description: constexpr std::addressof

#include <memory>
constexpr int x = 42;
constexpr const int* p = std::addressof(x);
auto main() -> int { return *p - 42; }
