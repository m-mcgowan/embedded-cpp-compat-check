// feature: freestanding_algorithm
// macro: __cpp_lib_freestanding_algorithm
// standard: cpp23
// category: library
// description: Freestanding algorithm subset

#include <algorithm>
auto main() -> int {
#ifdef __cpp_lib_freestanding_algorithm
  return 0;
#else
  return 0;
#endif
}
