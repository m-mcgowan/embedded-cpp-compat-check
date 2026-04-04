// feature: attr_indeterminate
// macro: __has_cpp_attribute(indeterminate)
// standard: cpp23
// category: attribute
// description: [[indeterminate]] attribute

auto main() -> int {
#if __has_cpp_attribute(indeterminate)
  [[indeterminate]] int x;
  (void)x;
#endif
  return 0;
}
