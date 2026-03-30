// feature: generator
// macro: __cpp_lib_generator
// standard: cpp23
// category: library
// description: std::generator

#include <generator>
#include <ranges>
std::generator<int> iota(int n) { for (int i=0; i<n; ++i) co_yield i; }
auto main() -> int { int s=0; for (auto i : iota(4)) s+=i; return s-6; }
