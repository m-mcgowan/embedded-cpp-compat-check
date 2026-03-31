// feature: to_chars
// macro: __cpp_lib_to_chars
// standard: cpp14
// category: library
// description: std::to_chars / std::from_chars

#include <charconv>
#include <array>
auto main() -> int { std::array<char, 16> buf; auto [ptr, ec] = std::to_chars(buf.data(), buf.data() + buf.size(), 42); return ec == std::errc{} ? 0 : 1; }
