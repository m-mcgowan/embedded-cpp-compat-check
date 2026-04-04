// feature: freestanding_feature_test_macros
// macro: __cpp_lib_freestanding_feature_test_macros
// standard: cpp23
// category: library
// description: Support for freestanding feature-test macros

#include <version>
auto main() -> int {
#ifdef __cpp_lib_freestanding_feature_test_macros
  return 0;
#else
  return 0;
#endif
}
