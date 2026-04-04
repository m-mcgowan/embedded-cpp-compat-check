// feature: static_assert_
// macro: __cpp_static_assert
// standard: cpp11
// category: language
// description: static_assert

static_assert(sizeof(int) >= 2, "int too small");
auto main() -> int { return 0; }
