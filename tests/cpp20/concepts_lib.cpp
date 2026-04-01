// feature: concepts_lib
// macro: __cpp_lib_concepts
// standard: cpp20
// category: library
// description: Standard library concepts (<concepts> header)

#include <concepts>
template<std::integral T> T add(T a, T b) { return a + b; }
auto main() -> int { return add(2, 3) - 5; }
