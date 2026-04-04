// feature: trivial_union
// macro: __cpp_trivial_union
// standard: cpp23
// category: language
// description: Trivial union

#include <version>
auto main() -> int {
#ifdef __cpp_trivial_union
  return 0;
#else
  return 0;
#endif
}
