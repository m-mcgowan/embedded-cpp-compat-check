// feature: move_only_function
// macro: __cpp_lib_move_only_function
// standard: cpp23
// category: library
// description: std::move_only_function

#include <functional>
auto main() -> int { std::move_only_function<int()> f = []{ return 42; }; return f() - 42; }
