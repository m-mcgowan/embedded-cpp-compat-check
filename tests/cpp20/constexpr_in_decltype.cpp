// feature: constexpr_in_decltype
// macro: __cpp_constexpr_in_decltype
// standard: cpp20
// category: language
// description: constexpr evaluation in decltype

constexpr int val = 42;
auto main() -> int { decltype(val + 1) x = val; return x - 42; }
