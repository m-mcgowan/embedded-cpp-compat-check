// feature: parallel_algorithm
// macro: __cpp_lib_parallel_algorithm
// standard: cpp17
// category: library
// description: #include <execution>, std::execution::seq exists

#include <execution>
auto main() -> int { auto policy = std::execution::seq; (void)policy; return 0; }
