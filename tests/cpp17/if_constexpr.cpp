// feature: if_constexpr
// macro: __cpp_if_constexpr
// standard: cpp17
// category: language
// description: constexpr if statements

template<typename T>
auto to_int(T val) -> int {
    if constexpr (sizeof(T) > 4) {
        return static_cast<int>(val >> 32);
    } else {
        return static_cast<int>(val);
    }
}

auto main() -> int {
    return to_int(0);
}
