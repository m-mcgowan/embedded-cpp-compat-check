// feature: attr_likely
// macro: __has_cpp_attribute(likely)
// standard: cpp20
// category: attribute
// description: [[likely]] attribute

auto main() -> int { int x = 42; if (x == 42) [[likely]] { return 0; } return 1; }
