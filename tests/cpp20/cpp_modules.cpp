// feature: cpp_modules
// macro: __cpp_modules
// standard: cpp20
// category: language
// description: Module support (check via <version> header)

#include <version>
auto main() -> int {
#ifdef __cpp_modules
  return 0;
#else
  return 0;
#endif
}
