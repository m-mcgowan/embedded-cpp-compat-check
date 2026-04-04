// feature: attr_deprecated
// macro: __has_cpp_attribute(deprecated)
// standard: cpp23
// category: attribute
// description: [[deprecated]] attribute

[[deprecated]] void old_func() {}
auto main() -> int { return 0; }
