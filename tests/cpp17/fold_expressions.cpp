// feature: fold_expressions
// macro: __cpp_fold_expressions
// standard: cpp17
// category: language
// description: Fold expressions

template<typename... Args>
auto sum(Args... args) -> int {
    return (args + ...);
}

auto main() -> int {
    return sum(1, 2, 3) - 6;
}
