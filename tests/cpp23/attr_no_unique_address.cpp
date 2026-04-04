// feature: attr_no_unique_address
// macro: __has_cpp_attribute(no_unique_address)
// standard: cpp23
// category: attribute
// description: [[no_unique_address]] attribute

struct Empty {};
struct S { [[no_unique_address]] Empty e; int v; };
auto main() -> int { S s; s.v = 42; return s.v - 42; }
