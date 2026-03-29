// feature: as_const
// macro: __cpp_lib_as_const
// standard: cpp17
// category: library
// description: std::as_const

#include <utility>
#include <type_traits>

auto main() -> int {
    int x = 42;
    static_assert(std::is_const<std::remove_reference_t<decltype(std::as_const(x))>>::value, "");
    return std::as_const(x) - 42;
}
