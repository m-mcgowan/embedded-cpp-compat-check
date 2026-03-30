// feature: is_null_pointer
// macro: __cpp_lib_is_null_pointer
// standard: cpp14
// category: library
// description: std::is_null_pointer

#include <type_traits>
auto main() -> int { return std::is_null_pointer<decltype(nullptr)>::value ? 0 : 1; }
