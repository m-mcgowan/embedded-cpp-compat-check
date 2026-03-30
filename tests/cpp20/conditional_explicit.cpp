// feature: conditional_explicit
// macro: __cpp_conditional_explicit
// standard: cpp20
// category: language
// description: explicit(bool)

#include <type_traits>
struct S { template<typename T> explicit(!std::is_same_v<T, int>) S(T) {} };
auto main() -> int { S s(42); return 0; }
