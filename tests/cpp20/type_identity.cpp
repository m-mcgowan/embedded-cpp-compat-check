// feature: type_identity
// macro: __cpp_lib_type_identity
// standard: cpp20
// category: library
// description: std::type_identity

#include <type_traits>
template<typename T> void f(T, std::type_identity_t<T>) {}
auto main() -> int { f(1, 2); return 0; }
