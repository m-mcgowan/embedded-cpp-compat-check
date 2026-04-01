// feature: assume_aligned
// macro: __cpp_lib_assume_aligned
// standard: cpp20
// category: library
// description: std::assume_aligned

#include <memory>
auto main() -> int { alignas(64) int buf[4] = {42}; auto* p = std::assume_aligned<64>(buf); return p[0] - 42; }
