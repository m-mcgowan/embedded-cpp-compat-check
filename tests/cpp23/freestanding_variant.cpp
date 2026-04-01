// feature: freestanding_variant
// macro: __cpp_lib_freestanding_variant
// standard: cpp23
// category: library
// description: Freestanding <variant>

#include <variant>
auto main() -> int {
#ifdef __cpp_lib_freestanding_variant
  return 0;
#else
  return 0;
#endif
}
