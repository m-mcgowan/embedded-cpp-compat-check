// feature: variable_templates
// macro: __cpp_variable_templates
// standard: cpp14
// category: language
// description: Variable templates

template<typename T>
constexpr T pi = T(3.1415926535897932385L);

auto main() -> int {
    return pi<int> - 3;
}
