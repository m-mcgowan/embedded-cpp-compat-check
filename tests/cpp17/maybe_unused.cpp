// feature: maybe_unused
// macro: __has_cpp_attribute(maybe_unused)
// standard: cpp17
// category: attribute
// description: [[maybe_unused]] attribute

auto main() -> int { [[maybe_unused]] int x = 42; return 0; }
