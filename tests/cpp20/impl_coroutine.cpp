// feature: impl_coroutine
// macro: __cpp_impl_coroutine
// standard: cpp20
// category: language
// description: Coroutines (compiler support)

#if __has_include(<coroutine>)
#include <coroutine>
#else
#include <experimental/coroutine>
#endif
auto main() -> int { return 0; }
