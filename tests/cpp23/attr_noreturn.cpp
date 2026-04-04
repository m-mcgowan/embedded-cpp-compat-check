// feature: attr_noreturn
// macro: __has_cpp_attribute(noreturn)
// standard: cpp23
// category: attribute
// description: [[noreturn]] attribute

[[noreturn]] void die() { while(true) {} }
auto main() -> int { return 0; }
