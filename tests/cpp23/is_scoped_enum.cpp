// feature: is_scoped_enum
// macro: __cpp_lib_is_scoped_enum
// standard: cpp23
// category: library
// description: std::is_scoped_enum

#include <type_traits>
enum A { X }; enum class B { Y };
auto main() -> int { return std::is_scoped_enum_v<B> && !std::is_scoped_enum_v<A> ? 0 : 1; }
