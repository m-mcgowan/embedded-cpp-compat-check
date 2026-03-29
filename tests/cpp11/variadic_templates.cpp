// feature: variadic_templates
// macro: __cpp_variadic_templates
// standard: cpp11
// category: language
// description: Variadic templates

template<typename... Args>
int count_args(Args...) { return sizeof...(Args); }

auto main() -> int {
    return count_args(1, 2, 3) - 3;
}
