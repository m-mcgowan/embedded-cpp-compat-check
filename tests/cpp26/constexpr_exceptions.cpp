// feature: constexpr_exceptions
// macro: __cpp_constexpr_exceptions
// standard: cpp26
// category: language
// description: constexpr exception handling

auto main() -> int {
#ifdef __cpp_constexpr_exceptions
  return 0;
#else
  return 0;
#endif
}
