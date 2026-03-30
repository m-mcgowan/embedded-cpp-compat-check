// feature: hex_float
// macro: __cpp_hex_float
// standard: cpp17
// category: language
// description: Hexadecimal floating literals

auto main() -> int { double d = 0x1.0p0; return d == 1.0 ? 0 : 1; }
