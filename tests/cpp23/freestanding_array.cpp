// feature: freestanding_array
// macro: __cpp_lib_freestanding_array
// standard: cpp23
// category: library
// description: Freestanding <array>

#include <array>
auto main() -> int {
#ifdef __cpp_lib_freestanding_array
  return 0;
#else
  return 0;
#endif
}
