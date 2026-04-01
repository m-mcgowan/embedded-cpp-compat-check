// feature: freestanding_cstring
// macro: __cpp_lib_freestanding_cstring
// standard: cpp23
// category: library
// description: Freestanding <cstring>

#include <cstring>
auto main() -> int {
#ifdef __cpp_lib_freestanding_cstring
  return 0;
#else
  return 0;
#endif
}
