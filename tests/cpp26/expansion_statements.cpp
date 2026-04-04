// feature: expansion_statements
// macro: __cpp_expansion_statements
// standard: cpp26
// category: language
// description: Expansion statements

auto main() -> int {
#ifdef __cpp_expansion_statements
  return 0;
#else
  return 0;
#endif
}
