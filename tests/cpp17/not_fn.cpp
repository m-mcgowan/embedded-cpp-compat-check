// feature: not_fn
// macro: __cpp_lib_not_fn
// standard: cpp17
// category: library
// description: std::not_fn
#include <functional>
bool is_even(int n) { return n % 2 == 0; }
auto main() -> int {
    auto is_odd = std::not_fn(is_even);
    return is_odd(3) ? 0 : 1;
}
