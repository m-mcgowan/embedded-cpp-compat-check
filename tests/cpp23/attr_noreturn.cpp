// feature: attr_noreturn
// macro: __has_cpp_attribute(noreturn)
// standard: cpp23
// category: attribute
// description: [[noreturn]] attribute

[[noreturn]] void die() { throw 42; }
auto main() -> int { return 0; }
