// feature: constexpr_charconv
// macro: __cpp_lib_constexpr_charconv
// standard: cpp23
// category: library
// description: constexpr std::to_chars

#include <charconv>
#include <array>
constexpr int f() { std::array<char, 16> buf{}; auto [ptr, ec] = std::to_chars(buf.data(), buf.data() + buf.size(), 42); return ec == std::errc{} ? 0 : 1; }
static_assert(f() == 0);
auto main() -> int { return 0; }
