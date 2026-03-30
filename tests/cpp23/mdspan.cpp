// feature: mdspan
// macro: __cpp_lib_mdspan
// standard: cpp23
// category: library
// description: std::mdspan

#include <mdspan>
auto main() -> int { int data[] = {1,2,3,4}; std::mdspan m(data, 2, 2); return m[1, 1] - 4; }
