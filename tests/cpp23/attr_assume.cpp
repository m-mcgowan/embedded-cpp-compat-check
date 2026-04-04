// feature: attr_assume
// macro: __has_cpp_attribute(assume)
// standard: cpp23
// category: attribute
// description: [[assume]] attribute

auto main() -> int {
#if __has_cpp_attribute(assume)
  int x = 42; [[assume(x == 42)]];
#endif
  return 0;
}
