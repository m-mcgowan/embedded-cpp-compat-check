// feature: freestanding_string_view
// macro: __cpp_lib_freestanding_string_view
// standard: cpp23
// category: library
// description: Freestanding <string_view>

#include <string_view>
auto main() -> int {
#ifdef __cpp_lib_freestanding_string_view
  return 0;
#else
  return 0;
#endif
}
