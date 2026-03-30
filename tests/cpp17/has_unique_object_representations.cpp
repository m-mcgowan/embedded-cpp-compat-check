// feature: has_unique_object_representations
// macro: __cpp_lib_has_unique_object_representations
// standard: cpp17
// category: library
// description: std::has_unique_object_representations

#include <type_traits>
auto main() -> int { return std::has_unique_object_representations_v<int> ? 0 : 1; }
