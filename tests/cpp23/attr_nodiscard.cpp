// feature: attr_nodiscard
// macro: __has_cpp_attribute(nodiscard)
// standard: cpp23
// category: attribute
// description: [[nodiscard]] attribute

[[nodiscard]] int compute() { return 42; }
auto main() -> int { int v = compute(); return v - 42; }
