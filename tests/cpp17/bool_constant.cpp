// feature: bool_constant
// macro: __cpp_lib_bool_constant
// standard: cpp17
// category: library
// description: std::bool_constant
#include <type_traits>
auto main() -> int {
    using t = std::bool_constant<true>;
    return t::value ? 0 : 1;
}
