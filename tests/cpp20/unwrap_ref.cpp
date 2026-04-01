// feature: unwrap_ref
// macro: __cpp_lib_unwrap_ref
// standard: cpp20
// category: library
// description: std::unwrap_reference and std::unwrap_ref_decay

#include <type_traits>
auto main() -> int { int x = 42; auto ref = std::ref(x); using T = std::unwrap_ref_decay_t<decltype(ref)>; return std::is_same_v<T, int&> ? 0 : 1; }
