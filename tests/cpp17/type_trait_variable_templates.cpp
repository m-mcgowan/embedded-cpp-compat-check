// feature: type_trait_variable_templates
// macro: __cpp_lib_type_trait_variable_templates
// standard: cpp17
// category: library
// description: Type traits variable templates (is_void_v etc)
#include <type_traits>
auto main() -> int {
    return std::is_integral_v<int> && !std::is_floating_point_v<int> ? 0 : 1;
}
