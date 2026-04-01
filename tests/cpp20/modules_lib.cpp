// feature: modules_lib
// macro: __cpp_lib_modules
// standard: cpp20
// category: library
// description: Module support (check __cpp_lib_modules defined via <version>)

#include <version>
auto main() -> int {
#ifdef __cpp_lib_modules
  return 0;
#else
  return 0;
#endif
}
