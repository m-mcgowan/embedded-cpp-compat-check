// feature: out_ptr
// macro: __cpp_lib_out_ptr
// standard: cpp23
// category: library
// description: std::out_ptr and std::inout_ptr

#include <memory>
static void alloc_int(int** p) { *p = new int(42); }
auto main() -> int { std::unique_ptr<int> up; alloc_int(std::out_ptr(up)); return *up - 42; }
