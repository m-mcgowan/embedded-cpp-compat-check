// feature: start_lifetime_as
// macro: __cpp_lib_start_lifetime_as
// standard: cpp23
// category: library
// description: std::start_lifetime_as

#include <memory>
auto main() -> int {
#ifdef __cpp_lib_start_lifetime_as
  alignas(int) unsigned char buf[sizeof(int)] = {42, 0, 0, 0};
  int* p = std::start_lifetime_as<int>(buf);
  (void)p;
  return 0;
#else
  return 0;
#endif
}
