// feature: forward_like
// macro: __cpp_lib_forward_like
// standard: cpp23
// category: library
// description: std::forward_like
#include <utility>
#include <type_traits>
struct S { int x; };
auto main() -> int {
    S s{42};
    auto&& ref = std::forward_like<const S&>(s.x);
    return ref - 42;
}
