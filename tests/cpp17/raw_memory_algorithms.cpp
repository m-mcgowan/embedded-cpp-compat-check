// feature: raw_memory_algorithms
// macro: __cpp_lib_raw_memory_algorithms
// standard: cpp17
// category: library
// description: std::uninitialized_move, uninitialized_value_construct etc

#include <memory>
auto main() -> int { int src[] = {1,2,3}; alignas(int) unsigned char buf[sizeof(src)]; auto* dst = reinterpret_cast<int*>(buf); std::uninitialized_copy(src, src+3, dst); int v = dst[0] + dst[1] + dst[2]; std::destroy(dst, dst+3); return v - 6; }
