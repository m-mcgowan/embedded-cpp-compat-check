// feature: freestanding_expected
// macro: __cpp_lib_freestanding_expected
// standard: cpp23
// category: library
// description: Freestanding <expected>

#include <expected>
auto main() -> int {
#ifdef __cpp_lib_freestanding_expected
  return 0;
#else
  return 0;
#endif
}
