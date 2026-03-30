// feature: is_invocable
// macro: __cpp_lib_is_invocable
// standard: cpp17
// category: library
// description: std::is_invocable and std::invoke_result

#include <type_traits>
int add(int a, int b) { return a+b; }
auto main() -> int { return std::is_invocable_v<decltype(add), int, int> ? 0 : 1; }
