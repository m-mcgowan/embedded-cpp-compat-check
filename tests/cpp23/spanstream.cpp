// feature: spanstream
// macro: __cpp_lib_spanstream
// standard: cpp23
// category: library
// description: std::spanstream — stream over a fixed buffer

#include <spanstream>
auto main() -> int { char buf[32]; std::ospanstream ss(buf); ss << 42; return 0; }
