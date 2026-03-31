// feature: reference_from_temporary
// macro: __cpp_lib_reference_from_temporary
// standard: cpp23
// category: library
// description: std::reference_constructs_from_temporary

#include <type_traits>
auto main() -> int { return std::reference_constructs_from_temporary_v<const int&, int> ? 0 : 1; }
