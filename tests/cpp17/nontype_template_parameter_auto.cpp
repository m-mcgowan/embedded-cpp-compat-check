// feature: nontype_template_parameter_auto
// macro: __cpp_nontype_template_parameter_auto
// standard: cpp17
// category: language
// description: auto non-type template parameters

template<auto N> constexpr auto value = N;
auto main() -> int { return value<42> - 42; }
