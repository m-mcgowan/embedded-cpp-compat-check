// feature: size_t_suffix
// macro: __cpp_size_t_suffix
// standard: cpp23
// category: language
// description: Literal suffixes for size_t

auto main() -> int { auto n = 42uz; return n == 42 ? 0 : 1; }
