// feature: transformation_trait_aliases
// macro: __cpp_lib_transformation_trait_aliases
// standard: cpp14
// category: library
// description: TransformationTrait aliases (remove_const_t etc)

#include <type_traits>
auto main() -> int { return std::is_same<std::remove_const_t<const int>, int>::value ? 0 : 1; }
