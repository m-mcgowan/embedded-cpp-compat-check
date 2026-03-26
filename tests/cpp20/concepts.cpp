// feature: concepts
// macro: __cpp_concepts
// standard: cpp20
// category: language
// description: Concepts

#include <concepts>

template<typename T>
concept Addable = requires(T a, T b) { { a + b } -> std::convertible_to<T>; };

template<Addable T>
auto add(T a, T b) -> T { return a + b; }

auto main() -> int {
    return add(1, 2) - 3;
}
