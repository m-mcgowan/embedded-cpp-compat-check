// feature: result_of_sfinae
// macro: __cpp_lib_result_of_sfinae
// standard: cpp14
// category: library
// description: std::result_of and SFINAE

#include <type_traits>
int f(int x) { return x; }
auto main() -> int { return std::is_same<std::result_of<decltype(f)(int)>::type, int>::value ? 0 : 1; }
