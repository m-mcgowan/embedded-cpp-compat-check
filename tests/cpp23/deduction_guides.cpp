// feature: deduction_guides
// macro: __cpp_lib_deduction_guides
// standard: cpp23
// category: library
// description: Deduction guides

#include <version>
auto main() -> int {
#ifdef __cpp_lib_deduction_guides
  return 0;
#else
  return 0;
#endif
}
