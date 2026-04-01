// feature: freestanding_optional
// macro: __cpp_lib_freestanding_optional
// standard: cpp23
// category: library
// description: Freestanding <optional>

#include <optional>
auto main() -> int {
#ifdef __cpp_lib_freestanding_optional
  return 0;
#else
  return 0;
#endif
}
