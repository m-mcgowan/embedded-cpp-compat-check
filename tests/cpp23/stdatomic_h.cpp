// feature: stdatomic_h
// macro: __cpp_lib_stdatomic_h
// standard: cpp23
// category: library
// description: C-compatible <stdatomic.h> header

#include <stdatomic.h>
auto main() -> int { atomic_int a = 0; atomic_store(&a, 42); return atomic_load(&a) - 42; }
