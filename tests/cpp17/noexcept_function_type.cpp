// feature: noexcept_function_type
// macro: __cpp_noexcept_function_type
// standard: cpp17
// category: language
// description: noexcept as part of function type

#include <type_traits>
auto main() -> int { return std::is_same_v<void() noexcept, void()> ? 1 : 0; }
