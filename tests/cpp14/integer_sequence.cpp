// feature: integer_sequence
// macro: __cpp_lib_integer_sequence
// standard: cpp14
// category: library
// description: Compile-time integer sequences

#include <utility>

template<typename T>
constexpr T sum_impl(T val) { return val; }

template<typename T, typename... Rest>
constexpr T sum_impl(T val, Rest... rest) { return val + sum_impl<T>(rest...); }

template<typename T, T... Ints>
constexpr T sum_seq(std::integer_sequence<T, Ints...>) { return sum_impl<T>(Ints...); }

auto main() -> int {
    // 0+1+2+3 = 6
    return sum_seq(std::make_index_sequence<4>{}) - 6;
}
