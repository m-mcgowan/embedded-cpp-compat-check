// feature: optional
// macro: __cpp_lib_optional
// standard: cpp17
// category: library
// description: std::optional

#include <optional>

auto main() -> int {
    std::optional<int> val = 42;
    return val.value() - 42;
}
