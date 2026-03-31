// feature: coroutine
// macro: __cpp_lib_coroutine
// standard: cpp20
// category: library
// description: Coroutine support library <coroutine>

#include <coroutine>
auto main() -> int { std::coroutine_handle<> h; (void)h; return 0; }
