// feature: jthread
// macro: __cpp_lib_jthread
// standard: cpp20
// category: library
// description: std::jthread and std::stop_token

#include <stop_token>
auto main() -> int { std::stop_source src; std::stop_token tok = src.get_token(); return tok.stop_requested() ? 1 : 0; }
