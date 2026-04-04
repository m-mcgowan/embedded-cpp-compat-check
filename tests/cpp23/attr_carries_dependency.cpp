// feature: attr_carries_dependency
// macro: __has_cpp_attribute(carries_dependency)
// standard: cpp23
// category: attribute
// description: [[carries_dependency]] attribute

[[carries_dependency]] int load(int* p) { return *p; }
auto main() -> int { int v = 42; return load(&v) - 42; }
