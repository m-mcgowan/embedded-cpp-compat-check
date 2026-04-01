// feature: constexpr_typeinfo
// macro: __cpp_lib_constexpr_typeinfo
// standard: cpp23
// category: library
// description: constexpr typeid

#include <typeinfo>
auto main() -> int { constexpr auto& ti = typeid(int); return ti == typeid(int) ? 0 : 1; }
