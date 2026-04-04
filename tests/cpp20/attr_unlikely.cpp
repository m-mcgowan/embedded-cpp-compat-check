// feature: attr_unlikely
// macro: __has_cpp_attribute(unlikely)
// standard: cpp20
// category: attribute
// description: [[unlikely]] attribute

auto main() -> int { int x = 42; if (x != 42) [[unlikely]] { return 1; } return 0; }
