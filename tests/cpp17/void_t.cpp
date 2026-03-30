// feature: void_t
// macro: __cpp_lib_void_t
// standard: cpp17
// category: library
// description: std::void_t
#include <type_traits>
template<typename, typename = std::void_t<>>
struct has_type : std::false_type {};
template<typename T>
struct has_type<T, std::void_t<typename T::type>> : std::true_type {};
struct A { using type = int; };
auto main() -> int { return has_type<A>::value ? 0 : 1; }
