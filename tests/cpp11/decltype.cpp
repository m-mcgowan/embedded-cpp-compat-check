// feature: decltype
// macro: __cpp_decltype
// standard: cpp11
// category: language
// description: decltype specifier

auto main() -> int { int x = 42; decltype(x) y = x; return y - 42; }
